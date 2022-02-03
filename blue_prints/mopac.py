from typing import List

from brick_yard.blue_print import BluePrint, EnvVars


class mopac(BluePrint):
    """
    MOPAC -- A semi-emperical QM backend
    """

    name = "mopac"
    version = "2016"

    def source(self, env: EnvVars) -> List[str]:

        env.zip_name = f"MOPAC{env.version}_for_Linux_64_bit.zip"

        return [f"wget http://openmopac.net/{env.zip_name} -P {env.source_path}"]

    def install(self, env: EnvVars) -> List[str]:
        return [
            f"mkdir -p {env.install_path}/bin",
            f"unzip {env.source_path}/{env.zip_name} -d {env.install_path}/bin/",
            f"chmod u+x {env.install_path}/bin/MOPAC{env.version}.exe",
        ]
