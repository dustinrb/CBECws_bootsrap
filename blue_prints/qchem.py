from typing import List

from brick_yard.blue_print import CMakeBluePrint, EnvVars


def add_qcsvn_url(env: EnvVars):
    env.svn_root = f"https://jubilee.q-chem.com/svnroot/{env.name}"

    if env.get_var("version") == "trunk":
        env.source_url = f"{env.svn_root}/{env.version}"
    else:
        env.source_url = f"{env.svn_root}/branches/{env.version}"


class qchem(CMakeBluePrint):
    """
    qchem -- QChem software package. Clones from SVN
    """

    name = "qchem"
    version = "trunk"
    required_env = [
        "MKLROOT",
    ]
    required_lmod = [
        "intel",
        "hdf5",
        "cmake",
    ]

    def source(self, env: EnvVars) -> List[str]:
        add_qcsvn_url(env)
        return [f"svn co {env.source_url} {env.source_path}"]

    def update(self, env: EnvVars) -> List[str]:
        return ["svn up"]

    def configure(self, env: EnvVars) -> List[str]:

        if env.get_var("build_tool") == "ninja":
            env.qc_build_tool_flag = "--ninja"
        else:
            env.qc_build_tool_flag = ""

        return [
            f"mkdir -p {env.build_path}",
            f"cd {env.build_path}",
            f"export QCBUILD=`realpath --relative-to={env.source_path} {env.build_path}`",
            # f"./configure intel mkl openmp relwdeb nointracule nomgc noccman2 "
            f"{env.source_path}/configure intel mkl openmp release {env.qc_build_tool_flag} --prefix={env.install_path}",
            f"cmake -B {env.build_path} -DCMAKE_EXPORT_COMPILE_COMMANDS=YES {env.source_path}",
        ]

    def build(self, env: EnvVars) -> List[str]:
        return [
            f"cmake --build {env.build_path} --target qcprog.exe -- -j {env.nprocs}"
        ]

    def install(self, env: EnvVars) -> List[str]:
        return [
            f"mkdir -p {env.install_path}/exe",
            # Manually install qcexe
            # Install debug version if we have it
            f"test -f {env.build_path}/qcprog.dbg && cp {env.build_path}/qcprog.dbg {env.install_path}/exe",
            # Install the main program
            f"cp {env.build_path}/qcprog.exe {env.install_path}/exe",
            # And the support scripts
            f"cp -r {env.source_path}/bin {env.install_path}",
            f"test -d {env.install_path}/bin/mpi || ln -s {env.source_path}/bin/mpi {env.install_path}/bin/mpi",
        ]
