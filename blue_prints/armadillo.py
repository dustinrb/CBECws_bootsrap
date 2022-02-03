from typing import List

from brick_yard.blue_print import CMakeBluePrint, EnvVars


class armadillo(CMakeBluePrint):
    """
    armadillo -- C++ matrix library in headers
    """

    name = "armadillo"
    version = "10.2.x"
    required_lmod = ["cmake", "intel"]

    def source(self, env: EnvVars) -> List[str]:
        return [
            f"git clone --branch {env.version} https://gitlab.com/conradsnicta/armadillo-code.git {env.source_path}"
        ]
