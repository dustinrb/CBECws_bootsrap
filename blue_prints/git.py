from typing import List

from brick_yard.blue_print import EnvVars, MakeBluePrint


class git(MakeBluePrint):
    """
    git -- newer version of git needed for VSCode
    """

    name = "git"
    version = "2.35.1"
    required_lmod = ["gcc"]

    def source(self, env: EnvVars) -> List[str]:
        return [
            f"git clone --branch v{env.version} https://github.com/git/git.git {env.source_path}"
        ]
