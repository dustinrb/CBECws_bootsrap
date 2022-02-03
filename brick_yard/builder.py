import subprocess
from datetime import datetime
from os import environ
from pathlib import Path
from shlex import quote
from subprocess import PIPE
from typing import List

from brick_yard.blue_print import BluePrint, EnvVars
from brick_yard.lmod import is_loaded

CORE_ENV = [
    "SOURCE_PATH",
    "ENV_PATH",
    "BUILD_PATH",
    "USER_MODFILES",
    "BUILD_SCRIPTS",  # Path to this package
]


class BuildRunner(object):
    build_script: str

    front_matter: List[str]
    cmds: List[str]
    env: EnvVars

    def __init__(self) -> None:
        self.build_script = ""
        self.front_matter = []
        self.cmds = []
        self.env = EnvVars()

    def set_env(self, env: EnvVars):
        self.env = env

    def run_job(self):
        for c in self.front_matter:
            self.out(c)

        self.out_block("ENVIRONMENT VARIABLES")
        for k, v in self.env.vars.items():
            if k in CORE_ENV:
                continue
            self.out(f'{k}="{v}"')

        self.out_block("COMMANDS")
        for cmd in self.cmds:
            self.out(cmd)

    def out(self, output):
        self.build_script += output + "\n"

    def out_block(self, msg):
        _msg = "#     " + msg + "     #"
        self.out("")
        self.out("#" * len(_msg))
        self.out(_msg)
        self.out("#" * len(_msg))

    def log(self, msg):
        _msg = "# {}".format(msg)
        self.cmds.append(_msg)

    def mkdir(self, directory):
        mk_cmd = "mkdir -p {}".format(directory)
        self.cmds.append(mk_cmd)

    def chdir(self, directory):
        cd_cmd = "cd {}".format(directory)
        self.cmds.append(cd_cmd)

    def section(self, title):
        self.cmds.append("")
        self.cmds.append("#### {} ####".format(title))

    def run(self, cmd):
        self.cmds.append(cmd)

    def add_front_matter(self, comment):
        self.front_matter.append("# {}".format(comment))


class PrintRunner(BuildRunner):
    def run_job(self):
        self.out("#!/bin/bash")
        self.out("")
        super().run_job()
        print(self.build_script)
        return 0


class BashRunner(BuildRunner):
    def run(self, output):
        super().run(f'echo "RUNNING: {quote(output)}"')
        return super().run(output)

    def run_job(self):
        super().out("#!/bin/bash")
        super().out("set -e")
        super().run_job()
        proc = subprocess.run(self.build_script, shell=True)
        return proc.returncode


def get_nprocs():
    # Ad-hock solution for handing supercomputer backends
    if "SLURM_NTASKS" in environ.keys():
        return environ["SLURM_NTASKS"]
    if "PBS_NP" in environ.keys():
        return environ["PBS_NP"]

    procs_cmd = subprocess.run("nproc", shell=True, stdout=PIPE)
    nprocs = procs_cmd.stdout.strip()
    return nprocs.decode("utf-8")


def get_global_env() -> EnvVars:
    env_var = EnvVars()
    for var in CORE_ENV:
        env_var.set_var(var, environ[var])
    env_var.nprocs = get_nprocs()
    if is_loaded("ninja"):
        env_var.cmake_build_tool = "Ninja"
        env_var.build_tool = "ninja"
    else:
        env_var.cmake_build_tool = "Unix Makefiles"
        env_var.build_tool = "make"
    return env_var


def add_front_matter(bp: BluePrint, runner: BuildRunner) -> None:
    # Print the global environment but don't declare them as variables
    runner.add_front_matter("SCRIPT GENERATED: {}".format(datetime.now().isoformat()))
    runner.add_front_matter(f"BLUE PRINT:\t{bp.name}")
    runner.add_front_matter(f"VERSION:\t{bp.version}")
    for var in CORE_ENV:
        runner.add_front_matter(f"{var}:\t{environ[var]}")


def build_bp(bp: BluePrint, runner: BuildRunner) -> None:

    # RUN ALL COMMANDS SO WE HAVE THE PROPER ENV AVAILABLE
    (
        source_cmds,
        update_cmds,
        configure_cmds,
        build_cmds,
        install_cmds,
        modfile_cmds,
        _uninstall_cmds,
    ) = bp.get_steps()

    env = bp.env
    runner.set_env(env)

    source_path = Path(environ["SOURCE_PATH"], bp.name, bp.version)
    build_path = Path(environ["BUILD_PATH"], bp.name, bp.version)
    install_path = Path(environ["ENV_PATH"], bp.name, bp.version)
    mod_file = Path(environ["USER_MODFILES"], bp.name, bp.version + ".lua")

    # NOW LOAD ALL THE REQUIREMENTS
    if bp.required_env:
        runner.section("REQUIRED ENV VARIABLES")
        for req in bp.required_env:
            runner.run(
                f'test -n "{req}" || {{ echo "MISSING REQUIRED ENV VAR {req}"; exit 1; }}'
            )

    if bp.required_lmod:
        runner.section("REQUIRED MODULES")
        for req in bp.required_lmod:
            runner.run(
                f'module is-loaded {req} || {{ echo "MISSING REQUIRE PACKAGE {req}"; exit 1; }}'
            )

    # RUN THE ACTUAL STEPS
    if not source_path.exists() and source_cmds:
        runner.section("FETCH SOURCE")
        runner.chdir(env.SOURCE_PATH)
        for c in source_cmds:
            runner.run(c)

    if not build_path.exists() and configure_cmds:
        runner.section("CONFIGURE PROJECT")
        runner.chdir(env.source_path)
        for c in configure_cmds:
            runner.run(c)

    if build_cmds:
        runner.section("BUILD PROJECT")
        runner.chdir(env.build_path)
        for c in build_cmds:
            runner.run(c)

    if install_cmds:
        runner.section("INSTALL SOFTWARE")
        for c in install_cmds:
            runner.run(c)

    if not mod_file.exists() and modfile_cmds:
        runner.section("ADDING MOD FILE")
        for c in modfile_cmds:
            runner.run(c)


def update_bp(bp: BluePrint, runner: BuildRunner) -> None:
    (
        _source_cmds,
        update_cmds,
        _configure_cmds,
        _build_cmds,
        _install_cmds,
        _modfile_cmds,
        _uninstall_cmds,
    ) = bp.get_steps()

    runner.set_env(bp.env)

    source_path = Path(environ["SOURCE_PATH"], bp.name, bp.version)

    if source_path.exists():
        runner.section(f"UPDATING SOURCE FOR {bp.name.upper()}")
        runner.chdir(bp.env.source_path)
        for c in update_cmds:
            runner.run(c)


def remove_bp(bp: BluePrint, runner: BuildRunner) -> None:
    (
        _source_cmds,
        _update_cmds,
        _configure_cmds,
        _build_cmds,
        _install_cmds,
        _modfile_cmds,
        uninstall_cmds,
    ) = bp.get_steps()

    runner.set_env(bp.env)

    runner.section(f"UNINSTALLING {bp.name.upper()}")
    for c in uninstall_cmds:
        runner.run(c)
