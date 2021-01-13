import subprocess

from os import environ as ENV, error
from subprocess import PIPE, STDOUT, DEVNULL

# LMOD
def is_loaded(pkg):
    LMDOD_CMD = ENV["LMOD_CMD"]
    
    # MPI has many impl. so we look for the family
    if pkg == "mpi" and get_MPI():
        return True

    _is_loaded = subprocess.run(
        [LMDOD_CMD, "is-loaded", pkg],
        stderr=DEVNULL,
        stdout=DEVNULL
    )
    return _is_loaded.returncode == 0

def get_compiler():
    compiler = ENV.get("LMOD_FAMILY_COMPILER", "")
    version = ENV.get("LMOD_FAMILY_COMPILER_VERSION", "")
    if compiler:
        return "{}/{}".format(compiler, version)
    return ""

def get_MPI():
    mpi = ENV.get("LMOD_FAMILY_MPI", "")
    version = ENV.get("LMOD_FAMILY_MPI_VERSION", "")
    if mpi:
        return "{}/{}".format(mpi, version)
    return ""    

def get_build_tool():
    bt = ENV.get("LMOD_FAMILY_MPI", "")
    version = ENV.get("LMOD_FAMILY_MPI_VERSION", "")
    if bt:
        return "{}/{}".format(bt, version)
    return ""