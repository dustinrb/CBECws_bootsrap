from typing import List

from blue_prints.qchem import add_qcsvn_url
from brick_yard.blue_print import BluePrint, EnvVars


class qcaux(BluePrint):
    """
    qcaux -- basis set definitions for QChem
    """

    name = "qcaux"
    version = "trunk"

    def source(self, env: EnvVars) -> List[str]:
        add_qcsvn_url(env)
        return [
            f"svn co {env.source_url} {env.install_path}",
            f"wget https://downloads.q-chem.com/qcinstall/drivers/drivers.linux.tar.gz -P {env.install_path}/",
            f"tar xzf {env.install_path}/drivers.linux.tar.gz -C {env.install_path}",
        ]

    def update(self, env: EnvVars) -> List[str]:
        return ["svn up"]
