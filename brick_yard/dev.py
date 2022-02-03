#! /usr/bin/python3
import json


def exclude_fortran(command):
    if command["file"].endswith(".F"):
        return False
    if command["file"].endswith(".F90"):
        return False
    return True


def clangify_compile_commands(ctx, path):
    with open(path, "r") as f:
        compile_commands = json.load(f)

    without_fortran = filter(exclude_fortran, compile_commands)
    compile_commands = list(without_fortran)

    for c in compile_commands:
        c["command"] = c["command"].replace("-qopenmp", "-fopenmp")

    print(json.dumps(compile_commands, indent=2, sort_keys=True))
