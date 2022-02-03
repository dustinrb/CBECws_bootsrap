from typing import List

from brick_yard.blue_print import CMakeBluePrint, EnvVars


class libint(CMakeBluePrint):
    """
    libint -- Integral library for QChem and CP2K
    """

    name = "libint"
    version = "2.7.1"
    required_lmod = ["cmake", "eigen"]

    def source(self, env: EnvVars) -> List[str]:
        env.base_folder = f"libint-{env.version}"
        env.tar_file = f"{env.base_folder}.tgz"
        env.url = f"https://github.com/evaleev/libint/releases/download/v{env.version}/{env.tar_file}"

        return [
            f"wget {env.url} -P {env.source_path}",
            f"tar -xf {env.source_path}/{env.tar_file} -C {env.source_path}",
            f"rm -rf {env.source_path}/{env.tar_file}",
            f"mv {env.source_path}/{env.base_folder}/* {env.source_path}",
        ]
