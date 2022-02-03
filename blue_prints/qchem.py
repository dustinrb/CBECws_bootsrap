from typing import List

from blue_prints.qchem import add_qcsvn_url
from brick_yard.blue_print import CMakeBluePrint, EnvVars


def add_qcsvn_url(env: EnvVars):
    env.svn_root = f"https://jubilee.q-chem.com/{env.name}"

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
    required_lmod = ["intel", "mkl", "cmake"]

    def source(self, env: EnvVars) -> List[str]:
        add_qcsvn_url(env)
        return [f"svn co {env.source_url} {env.source_path}"]

    def update(self, env: EnvVars) -> List[str]:
        return ["svn up"]

    def configure(self, env: EnvVars) -> List[str]:

        if env.get_var("build_tool") == "ninja":
            env.qc_build_tool_flag = env.build_tool
        else:
            env.qc_build_tool_flag = ""

        return [
            "export QCBUILD=`realpath relative-to={env.build_path} {env.source_path}`",
            # "./configure intel mkl openmp relwdeb nointracule nomgc noccman2 "
            f"./configure intel mkl openmp rel {env.qc_build_tool_flag} --prefix={env.install_path}",
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
            f"cp {env.build_path}/qcprog.dbg {env.install_path}/exe",
            f"cp {env.build_path}/qcprog.exe {env.install_path}/exe",
            f"cp -r {env.source_path}/bin {env.install_path}",
            f"[[ ! -L {env.install_path}/bin/mpi ]] && ln -s {env.source_path}/bin/mpi {env.install_path}/bin/mpi",
        ]
