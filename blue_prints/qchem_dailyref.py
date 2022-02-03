from typing import List

from blue_prints.qchem import add_qcsvn_url
from brick_yard.blue_print import BluePrint, EnvVars


class qchem_dailyref(BluePrint):
    """
    qchem_dailyref -- test file reference values for qchem
    """

    name = "qchem_dailyref"
    version = "trunk"

    def source(self, env: EnvVars) -> List[str]:
        add_qcsvn_url(env)
        return [f"svn co {env.source_url} {env.source_path}"]

    def update(self, env: EnvVars) -> List[str]:
        return ["svn up"]

    def install(self, env: EnvVars) -> List[str]:
        return [
            f"mkdir -p {env.ENV_PATH}/qchem_dailyref",
            f"[[ ! -L {env.install_path} ]] && ln -s {env.source_path} {env.install_path}",
            f"svn up {env.source_path}",
        ]
