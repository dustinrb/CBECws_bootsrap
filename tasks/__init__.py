from invoke import Collection
from tasks import build, dev, git_svn

ns = Collection(build, dev, git_svn)