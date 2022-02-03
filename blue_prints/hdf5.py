from typing import List

from brick_yard.blue_print import AutoToolsBluePrint, EnvVars


class hdf5(AutoToolsBluePrint):
    """
    HDF5 library needed for QChem
    """

    name = "hdf5"
    version = "1.12.1"

    def source(self, env: EnvVars) -> List[str]:

        env.version__short = self.version[0 : self.version.rfind(".")]
        env.base_folder = f"hdf5-{env.version}"
        env.tar_file = f"{env.base_folder}.tar.gz"
        env.url = f"https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-{env.version__short}/hdf5-{env.version}/src/{env.tar_file}"

        return [
            f"wget {env.url} -P {env.source_path}",
            f"tar -xf {env.source_path}/{env.tar_file} -C {env.source_path}",
            f"rm -rf {env.source_path}/{env.tar_file}",
            f"mv {env.source_path}/{env.base_folder}/* {env.source_path}",
        ]

    def configure(self, env: EnvVars) -> List[str]:
        return [
            f"mkdir -p {env.build_path}",
            f"cd {env.build_path}",
            f"{env.source_path}/configure --prefix={env.install_path} --enable-fortran --enable-cxx",
        ]
