#! /usr/bin/python3
import pkgs
from BuildRunner import PrintRunner, BashRunner


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build a wide array of software tools for CBC computers and OSC computers")

    parser.add_argument("--build", action="store_true", help="execute the command in bash")
    parser.add_argument("-v", "--version", nargs=1, default=None, help="the version you desire to build")
    parser.add_argument("package", help="the package you desire to build")

    args = parser.parse_args()

    pkg = args.package
    version = args.version
    run_build = args.build

    try:
        pkg_fn = getattr(pkgs, pkg)
    except:
        print("The package \"{}\" does not exist. The available packages are:".format(pkg))
        for name, fn in vars(pkgs).items():
            mod = getattr(fn, "__module__", "")
            if mod == pkgs.__name__:
                print("  ", name)
        exit()

    if version is None: 
        builder = pkg_fn()
    else:
        builder = pkg_fn(version[0])

    if run_build:
        builder.runner = BashRunner()
    else:
        builder.runner = PrintRunner()

    builder.run()
    print("BUILDING {} IS COMPLETE!".format(pkg))