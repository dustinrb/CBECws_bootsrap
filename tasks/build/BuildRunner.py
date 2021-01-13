import subprocess

from datetime import datetime
from subprocess import PIPE, STDOUT, DEVNULL

from os import environ as ENV

class BuildRunner(object):
    build_scrpt = ""

    front_matter = []
    env = []
    cmds = []

    def __init__(self):
        pass

    def out(self, output):
        self.build_scrpt += output + "\n"

    def get_nprocs(self):
        # Ad-hock solution for handing supercomputer backends
        if "SLURM_NTASKS" in ENV.keys():
            return ENV["SLURM_NTASKS"]
        if "PBS_NP" in ENV.keys():
            return ENV["PBS_NP"]
        
        procs_cmd = subprocess.run("nproc", shell=True, stdout=PIPE)
        nprocs = procs_cmd.stdout.strip()
        return nprocs.decode("utf-8")

    def run_job(self):
        self.out("# SCRIPT GENERATED: {}".format(
            datetime.now().isoformat()
        ))

        for c in self.front_matter:
            self.out(c)

        self.set_env("nprocs", self.get_nprocs())

        self.out_block("ENVIRONMENT BARIABLES")
        for e in self.env:
            self.out(e)

        self.out_block("COMMANDS")
        for cmd in self.cmds:
            self.out(cmd)

    def out_block(self, msg):
        _msg = "#     " + msg + "     #"
        self.out("")
        self.out("#"*len(_msg))
        self.out(_msg)
        self.out("#"*len(_msg))

    def log(self, msg):
        _msg = "# {}".format(msg)
        self.cmds.append(_msg)

    def set_env(self, key, val, export=False):
        exp = ""
        if export:
            exp = "export "
        self.env.append("{e}{k}=\"{v}\"".format(k=key, v=val, e=exp))

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
        super().run_job()
        print(self.build_scrpt)

class BashRunner(BuildRunner):
    def run_job(self):
        self.out("#! /bin/sh")
        self.out("set -e")
        super().run_job()
        subprocess.run(self.build_scrpt, shell=True)