import datetime

from os import environ as ENV, error
from os.path import dirname, isdir, isfile, expandvars, relpath, join as pathjoin

from tasks.build.BuildRunner import BuildRunner
from tasks.build.LMod import is_loaded

REQUIRED_ENV = [ 
    "SRC_PATH",
    "ENV_PATH",
    "BUILD_PATH",
    "BUILD_SCRIPTS" # Path to this package
]

# Support functions
def is_env_setup(required=REQUIRED_ENV):
    for r in required:
        if not r in ENV.keys():
            return False
    return True

def listify(var):
    if isinstance(var, list):
        return var
    if var:
        return [var]
    return []

# COMPILE COMMANDS
class BuildJob(object):
    source_cmd=["mkdir -p $pkg_source_path"]
    configure_cmd=["cmake -G\"$pkg_cmake_build_tool\" -B $pkg_build_path -DCMAKE_INSTALL_PREFIX=$pkg_install_path $pkg_src"]
    build_cmd=["cmake --build $pkg_build_path -j $nprocs"]
    install_cmd=["cmake --install $pkg_build_path"]

    def __init__(
        self,
        package,
        version,
        source_cmd=None,
        configure_cmd=None,
        build_cmd=None,
        install_cmd=None,
        required_pkgs=[],
        required_build_pkgs=[],
        runner=None
    ):
        self.package = package
        self.version = version
        if not source_cmd is None:
            self.source_cmd = listify(source_cmd)
        if not configure_cmd is None:
            self.configure_cmd = listify(configure_cmd)
        if not build_cmd is None:
            self.build_cmd = listify(build_cmd)
        if not install_cmd is None:
            self.install_cmd = listify(install_cmd)
        self.required_pkgs = required_pkgs
        self.required_build_pkgs = required_build_pkgs
        self.runner=runner

    def setup(self):
        # Setup the configuration file
        self.check_setup()

        self.runner.add_front_matter(
            "PACKAGE:\t{}".format(self.package))
        self.runner.add_front_matter(
            "VERSION:\t{}".format(self.version))
        self.runner.add_front_matter(
            "SRC_PATH:\t{}".format(ENV["SRC_PATH"]))
        self.runner.add_front_matter(
            "BUILD_PATH:\t{}".format(ENV["BUILD_PATH"]))
        self.runner.add_front_matter(
            "ENV_PATH:\t{}".format(ENV["ENV_PATH"]))

        self.create_env()

    def source(self):
        self.setup()
        self.get_source()

    def configure(self):
        self.source()
        self.run_configure()
    
    def build(self):
        self.configure()
        self.run_build()

    def install(self):
        self.build()
        self.run_install()
        self.generate_modfiles()

    def run(self):
        self.runner.run_job()

    def check_setup(self):
        if self.runner is None:
            raise error("Specify a Runner")

        if not is_env_setup():
            raise error("Environment is not properly setup. The following environment variables are required: {}".format(
                " ".format(REQUIRED_ENV)
            ))

        build_recs = [is_loaded(i) for i in self.required_build_pkgs]
        if not all(build_recs):
            raise error(
                "Make sure that the following build requirements are loaded: {}".format(
                    " ".join(self.required_build_pkgs)
                ))

        recs = [is_loaded(i) for i in self.required_pkgs]
        if not all(recs):
            raise error(
                "Make sure that the following runtime requirements are loaded: {}".format(
                    " ".join(self.required_pkgs)
                ))

    def create_env(self):
        self._src_path = pathjoin("$SRC_PATH", self.package, self.version)
        self._build_path = pathjoin("$BUILD_PATH", self.package, self.version)
        self._install_path = pathjoin("$ENV_PATH", self.package, self.version)

        # Make relative paths avaiable (looking at your q-chem)
        self._rel_src_to_build = relpath(
            expandvars(self._build_path),
            start=expandvars(self._src_path)
        )
        self._rel_build_to_install = relpath(
            expandvars(self._install_path),
            start=expandvars(self._build_path)
        )
        
        self.runner.set_env("pkg_name", self.package)
        self.runner.set_env("pkg_version", self.version) 
        self.runner.set_env("pkg_src", self._src_path)
        self.runner.set_env("pkg_build_path", self._build_path)
        self.runner.set_env("pkg_install_path", self._install_path)
        self.runner.set_env("pkg_rel_src_to_build", self._rel_src_to_build)
        self.runner.set_env("pkg_rel_build_to_install", self._rel_build_to_install)

        if is_loaded("ninja"):
            self.runner.set_env("pkg_cmake_build_tool", "Ninja")
            self.runner.set_env("pkg_build_tool", "ninja")
        else:
            self.runner.set_env("pkg_cmake_build_tool", "Unix Makefiles")
            self.runner.set_env("pkg_build_tool", "make")
    
    def run_cmds(self, cmds, section="", run_path="", paths=[]):
        if not cmds:
            return
        if section:
            self.runner.section(section)
        if run_path:
            _path = expandvars(run_path)
            if not isdir(_path):
                self.runner.mkdir(_path)
            self.runner.chdir(_path)
        if paths:
            for p in paths:
                _path = expandvars(p)
                if not isdir(_path):
                    self.runner.mkdir(_path)

        for c in cmds:
            self.runner.run(c)

    def get_source(self):
        if isdir(expandvars(self._src_path)):
            return
        self.run_cmds(
            self.source_cmd,
            section="GETTING SOURCE CODE",
            run_path=self._src_path,
        ) 

    def run_configure(self):
        self.run_cmds(
            self.configure_cmd,
            section="RUNNING CONFIGURATION STEPS",
            run_path=self._src_path,
            paths=[self._build_path]
        )

    def run_build(self):
        self.run_cmds(
            self.build_cmd,
            section="RUNNING BUILD STEPS",
            run_path=self._build_path
        )

    def run_install(self):
        self.run_cmds(
            self.install_cmd,
            section="RUNNING INSTALL STEPS",
            run_path=self._build_path
        )

    def generate_modfiles(self):
        if not "USER_MODFILES" in ENV.keys():
            self.runner.log("Define the USER_MODFILES environment variable to enable modfile creation")
            return
        modfiles = pathjoin("$BUILD_SCRIPTS", "modfiles")
        # TODO: Dynamic jodfile generation
        modfile_script = pathjoin(modfiles, "{}.lua".format(self.package)) 
        final_dir = pathjoin("$USER_MODFILES", self.package)
        final_script = pathjoin(final_dir, "{}.lua".format(self.version))
        if not isfile(expandvars(modfile_script)) or isfile(expandvars(final_script)):
            if not isfile(expandvars(final_script)):
                self.runner.log("No modfile exists for {}; expected at {}".format(
                    self.package,
                    modfile_script
                ))
            return

        self.runner.section("LINKING TO MODFILE") 
        self.runner.mkdir(final_dir)
        self.runner.run("ln -s {} {}".format(modfile_script, final_script))
        