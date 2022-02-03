from typing import List

from brick_yard.blue_print import BluePrint, EnvVars


class julia(BluePrint):
    """
    julia -- Julia programming language
    """

    name = "julia"
    version = "1.7.1"

    def source(self, env: EnvVars) -> List[str]:

        env.version__short = self.version[0 : self.version.rfind(".")]

        return [
            f"wget https://julialang-s3.julialang.org/bin/linux/x64/{env.version__short}/julia-{env.version}-linux-x86_64.tar.gz -P {env.source_path}"
        ]

    def install(self, env: EnvVars) -> List[str]:
        return [
            f"mkdir -p {env.install_path}",
            f"tar -xf {env.source_path}/julia-{env.version}-linux-x86_64.tar.gz -C {env.install_path}",
        ]
