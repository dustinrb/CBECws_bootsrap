from typing import List

from brick_yard.blue_print import BluePrint, EnvVars


class ninja(BluePrint):
    """
    ninja -- speedy (and silent) build tool which eased QChem compilation
    """

    name = "ninja"
    version = "1.10.2"

    def source(self, env: EnvVars) -> List[str]:
        return [
            f"wget https://github.com/ninja-build/ninja/releases/download/v{env.version}/ninja-linux.zip -P {env.source_path}"
        ]

    def install(self, env: EnvVars) -> List[str]:
        return [
            f"mkdir -p {env.install_path}/bin",
            f"unzip {env.source_path}/ninja-linux.zip -d {env.install_path}/bin/",
        ]
