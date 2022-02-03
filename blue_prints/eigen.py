from typing import List

from brick_yard.blue_print import CMakeBluePrint, EnvVars


class eigen(CMakeBluePrint):
    """
    eigen -- Header library for matrix operations
    """

    name = "eigen"
    version = "3.3.9"
    required_lmod = ["cmake"]

    def source(self, env: EnvVars) -> List[str]:
        return [
            f"git clone --branch {env.version} https://gitlab.com/libeigen/eigen.git {env.source_path}"
        ]
