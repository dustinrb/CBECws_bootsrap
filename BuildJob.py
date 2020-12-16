import datetime

from os import environ as ENV, error
from os.path import dirname, isdir, isfile, expandvars, relpath, join as pathjoin

from BuildRunner import BuildRunner
from LMod import is_loaded

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
    return [var]

# COMPILE COMMANDS
class BuildJob(object):
    source_cmd=["mkdir -p $pkg_source_path"]
    configure_cmd=[""]
    build_cmd=["cmake --build $pkg_build_path -- -j $nprocs"]
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

    def run(self):
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

        self.get_source()
        self.run_configure()
        self.run_build()
        self.run_install()
        self.generate_modfiles()
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
    
    def run_cmds(self, cmds):
        for c in cmds:
            self.runner.run(c)

    def get_source(self):
        self.runner.section("GETTING SOURCE CODE") 
        if not isdir(expandvars(self._src_path)):
            self.run_cmds(self.source_cmd)

    def run_configure(self):
        if isdir(expandvars(self._build_path)):
            return
        self.runner.section("RUNNING CONFIGURATION STEPS") 
        self.runner.mkdir(self._build_path)
        self.runner.chdir(self._src_path)
        self.run_cmds(self.configure_cmd)            

    def run_build(self):
        self.runner.section("RUNNING BUILD STEPS") 
        self.runner.chdir(self._build_path)
        self.run_cmds(self.build_cmd) 

    def run_install(self):
        self.runner.section("RUNNING INSTALL STEPS") 
        self.runner.chdir(self._build_path)
        self.run_cmds(self.install_cmd)

    def generate_modfiles(self):
        if not "USER_MODFILES" in ENV.keys():
            self.runner.log("Define the USER_MODFILES environment variable to enable modfile creation")
            return
        modfiles = pathjoin(dirname(__file__), "modfiles")
        # TODO: Dynamic jodfile generation
        modfile_script = pathjoin(modfiles, "{}.lua".format(self.package)) 
        final_dir = pathjoin(ENV["USER_MODFILES"], self.package)
        final_script = pathjoin(final_dir, "{}.lua".format(self.version))
        if not isfile(modfile_script) or isfile(expandvars(final_script)):
            # TODO: Raise error? or is this not vital?
            return

        self.runner.section("LINKING TO MODFILE") 
        self.runner.mkdir(final_dir)
        self.runner.run("ln -s {} {}".format(modfile_script, final_script))
        