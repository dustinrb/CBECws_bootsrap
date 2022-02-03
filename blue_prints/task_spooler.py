from typing import List

from brick_yard.blue_print import BluePrint, EnvVars


class task_spooler(BluePrint):
    """
    git -- newer version of git needed for VSCode
    """

    name = "task_spooler"
    version = "1.0.1"

    def source(self, env: EnvVars) -> List[str]:
        env.tar_name = f"ts-{env.version}.tar.gz"
        env.url = f"https://vicerveza.homeunix.net/~viric/soft/ts/{env.tar_name}"

        return [
            f"wget {env.url} -P {env.source_path}",
            f"tar -xf {env.source_path}/{env.tar_name} -C {env.source_path}",
            f"rm -rf {env.source_path}/{env.tar_name}",
        ]

    def build(self, env: EnvVars) -> List[str]:
        return [
            f"make -C {env.source_path}/ts-{env.version}"
            f" PREFIX={env.install_path} -j {env.nprocs}"
        ]

    def install(self, env: EnvVars) -> List[str]:
        return [
            f"make -C {env.source_path}/ts-{env.version}"
            f" PREFIX={env.install_path} install"
        ]
