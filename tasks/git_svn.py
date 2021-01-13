import os
from os.path import basename
from urllib.parse import urlparse, urlunparse
from invoke import task

@task
def lite_init(ctx, url, path=None, rev=None):
    path = path or os.getcwd()
    path = os.path.abspath(path)

    if os.path.exists(os.path.join(path, ".git")):
        print("Git repo exists.")
        return

    ctx.run("git svn init --no-minimize-url -T trunk {url} {path}".format(
        url=url,
        path=path
    ))
    os.chdir(path)

    if rev:
        ctx.run("git svn fetch -r{rev}:HEAD".format(
            url=url
        ))
    else:
        ctx.run("git svn fetch".format(
            url=url
        ))


@task
def add_branch(ctx, name, path=None, rev=1):
    """
    from: https://stackoverflow.com/questions/296975/how-do-i-tell-git-svn-about-a-remote-branch-created-after-i-fetched-the-repo
    """
    old_path = os.getcwd()
    path = path or os.getcwd()
    path = os.path.abspath(path)
    os.chdir(old_path)

    svn_url = get_svn_url(ctx)
    git_vars: str = ctx.run("git config --list --name-only", hide=True).stdout

    for l in git_vars.splitlines():
        if not l.startswith("svn-remote"):
            continue
        if l.split(".")[1] == name:
            print("The branch {} already exists".format(name))
            return

    url = os.path.join(urlunparse(svn_url), "branches", name)
    ctx.run("git config --add svn-remote.{branch}.url {url}".format(
        branch=name,
        url=url
    ))
    ctx.run("git config --add svn-remote.{branch}.fetch :refs/remotes/origin/{branch}".format(
        branch=name
    ))
    ctx.run("git svn fetch {branch}".format(branch=name))
    os.chdir(old_path)


@task
def refresh_ignore(ctx, path=None):
    """
    Reads svn:ignore property and adds it to externals 
    """
    ctx.run("git svn show-ignore > .git/info/exclude")
    externals = get_externals(ctx)

    with open(".git/info/exclude", "a") as f:
        f.write("\n\n# Ignoreing externals\n")
        for prefix, paths in externals.items():
            prefix = "/" + prefix
            f.write("\n# {}\n".format(prefix))

            for p in paths:
                _, _path = p.split(" ")
                ignore_path = os.path.join(prefix, _path)
                # Maybe do this without the shell...
                f.write(ignore_path + "\n")


@task
def refresh_externals(ctx, path=None):
    """
    check if all external repositories are present and are at the proper revision

    This does not remove extranious external repos?
    Maybe clone to .git directory and create symbolic links
    """
    path = path or os.getcwd()
    path = os.path.abspath(path)

    os.chdir(path)
    externals = get_externals(ctx) 
    svn_url = get_svn_url(ctx)

    for prefix, reps in externals.items():
        for rep in reps:
            url_path, out_path = rep.split()
            url_path, rev = url_path.split("@")
            url_path = url_path.lstrip("/")
            url = "{}://{}/{}".format(
                svn_url.scheme,
                svn_url.netloc,
                url_path
            )

            out_path = os.path.join(path, prefix, out_path)
            create_external(ctx, url, out_path, rev=rev)


def get_externals(ctx):
    key = "undef"
    externals = {key: []}
    res = ctx.run("git svn show-externals", hide=True)
    
    for line in res.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            key = line[1:].strip()
            key = key.lstrip("/")
            externals[key] = []
            continue

        externals[key].append(line)
    return externals


def create_external(ctx, url, destination, rev=None):
    repo_name = destination.split("/")[-1] # Get the folder we will be outputing
    source_path = os.path.abspath(
        os.path.join(".", ".git", "externals", repo_name)
    )

    old_cwd = os.getcwd()
    if not os.path.exists(source_path):
        print("Cloning external {}".format(url))
        ctx.run("git svn clone {url} {path}".format(
            url=url,
            path=source_path
        ))
    os.chdir(source_path)
    commit = ctx.run("git svn find-rev r{}".format(rev), hide=True).stdout
    ctx.run("git checkout {}".format(commit), hide=True)

    os.chdir(old_cwd)
    base_path = os.path.join("/", *destination.split("/")[0:-1])
    not os.path.exists(base_path) and os.makedirs(base_path)
    not os.path.exists(destination) and ctx.run("ln -s {} {}/".format(
        source_path,
        base_path
    ))


def get_svn_url(ctx):
    svn_url = None
    for l in ctx.run("git svn info", hide=True).stdout.splitlines():
        key = "Repository Root: "
        if l.startswith(key):
            svn_url = urlparse(l[len(key):])
        
    if not svn_url:
        raise Exception("The path `{}` is not a git-svn repo".format(os.getcwd()))

    return svn_url