from typing import List

from brick_yard.blue_print import BluePrint, EnvVars


class orca(BluePrint):
    """
    orca -- another (German) qc package
    """

    name = "orca"
    version = "5.0.2"

    def source(self, env: EnvVars) -> List[str]:
        base_folder = (
            f"orca_{self.version.replace('.', '_')}_linux_x86-64_shared_openmpi411"
        )
        env.base_folder = base_folder
        env.tar_file = f"{base_folder}.tar.xz"

        return [f"mkdir -p {env.source_path}"]

    def install(self, env: EnvVars) -> List[str]:
        return [
            # Guard statement to make sure we have the software
            f"test -f {env.source_path}/{env.tar_file}"
            f' || {{ echo "Download {env.tar_file} into {env.source_path}" ; exit 0; }}',

            # Extract
            f"mkdir -p {env.install_path}",
            f"tar -xf {env.source_path}/{env.tar_file} -C {env.install_path}",

            # Move the archive folder out into the install path
            f"mv {env.install_path}/{env.base_folder}/* {env.install_path}",
            f"rm -rf {env.install_path}/{env.base_folder}",
        ]
