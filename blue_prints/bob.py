from typing import List

from brick_yard.blue_print import BluePrint, EnvVars


class bob(BluePrint):
    name = "bob"
    version = "master"

    def install(self, env: EnvVars) -> List[str]:
        return [
            f"mkdir -p {env.ENV_PATH}",
            f"mkdir -p {env.SOURCE_PATH}",
            f"mkdir -p {env.BUILD_PATH}",
            f"mkdir -p {env.USER_MODFILES}",
            f"mkdir -p {env.install_path}/bin",
            f"ln -s {env.BUILD_SCRIPTS}/bob {env.install_path}/bin/bob",
        ]
