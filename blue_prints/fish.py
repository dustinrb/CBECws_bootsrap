from typing import List

from brick_yard.blue_print import CMakeBluePrint, EnvVars


class fish(CMakeBluePrint):
    """
    fish -- Shell that is vastly better than bash
    """

    name = "fish"
    version = "3.3.1"
    required_lmod = ["cmake", "intel"]

    def source(self, env: EnvVars) -> List[str]:
        return [
            f"git clone --branch {env.version} https://github.com/fish-shell/fish-shell.git {env.source_path}"
        ]

    def configure(self, env: EnvVars) -> List[str]:
        return [
            f'CC=gcc CXX=g++ cmake -B {env.build_path} -G"{env.cmake_build_tool}" -DCMAKE_INSTALL_PREFIX={env.install_path} {env.source_path}'
        ]
