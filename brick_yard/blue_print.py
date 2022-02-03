import json
from collections import OrderedDict
from copy import copy
from os import path
from pathlib import Path
from typing import Any, Dict, List, Tuple


class EnvVars:
    def __init__(self, prefix=None) -> None:
        super().__setattr__("vars", OrderedDict())
        super().__setattr__("prefix", prefix or "pkg_")

    def mk_key(self, k: str) -> str:
        return (self.prefix + k).upper()

    def __setattr__(self, __name: str, __value: Any) -> None:
        key = self.mk_key(__name)
        self.vars[key] = __value
        return super().__setattr__(__name, "$" + key)

    def set_var(self, name: str, value: Any) -> None:
        key = name
        self.vars[key] = value
        super().__setattr__(name, "$" + key)

    def get_var(self, name: str) -> Any:
        key = self.mk_key(name)
        return self.vars[key]


class BluePrint:

    # Vital information
    name: str = None
    version: str = None
    required_lmod: List[str] = []
    required_env: List[str] = []

    # Internal
    status: Dict[str, bool]
    source_path: Path
    build_path: Path
    install_path: Path
    mod_path: Path

    def __init__(
        self,
        global_env: OrderedDict,
        version: str = None,
        update=False,
    ) -> None:
        if version is not None:
            self.version = version
        self.do_update = update

        env: EnvVars = copy(global_env)
        env.name = self.name
        env.version = self.version

        nv_slug = Path(env.name, env.version)

        env.source_path = env.SOURCE_PATH / nv_slug
        env.build_path = env.BUILD_PATH / nv_slug
        env.install_path = env.ENV_PATH / nv_slug
        env.mod_source = path.join(env.BUILD_SCRIPTS, "modfiles", env.name + ".lua")
        env.mod_path = path.join(env.USER_MODFILES, env.name)
        env.mod_file = path.join(env.mod_path, env.version + ".lua")
        env.build_status_file = path.join(env.install_path, "build_status.json")
        # self.status = self.get_status()

        self.env = env

    # Programatic Steps
    def source(self, env: EnvVars) -> List[str]:
        return [f"mkdir -p {env.source_path}"]

    def update(self, env: EnvVars) -> List[str]:
        return []

    def configure(self, env: EnvVars) -> List[str]:
        return [f"mkdir -p {env.build_path}"]

    def build(self, env: EnvVars) -> List[str]:
        return []

    def install(self, env: EnvVars) -> List[str]:
        return []

    def modfile(self, env: EnvVars) -> List[str]:
        return [
            f"mkdir -p {env.mod_path}",
            f"test -f {env.mod_file} || ln -s {env.mod_source} {env.mod_file}",
        ]

    def uninstall(self, env: EnvVars) -> List[str]:
        return [
            f"rm -rf {env.source_path}",
            f"rm -rf {env.build_path}",
            f"rm -rf {env.install_path}",
            f"rm -rf {env.mod_file}",
        ]

    def get_steps(self) -> Tuple[List[str], ...]:
        return (
            self.source(self.env),
            self.update(self.env),
            self.configure(self.env),
            self.build(self.env),
            self.install(self.env),
            self.modfile(self.env),
            self.uninstall(self.env),
        )


class MakeBluePrint(BluePrint):
    def build(self, env: EnvVars) -> List[str]:
        return [f"make -C {env.source_path} -j {env.nprocs}"]

    def install(self, env: EnvVars) -> List[str]:
        return [f"make -C {env.source_path} prefix={env.install_path} install"]


class AutoToolsBluePrint(MakeBluePrint):
    def configure(self, env: EnvVars) -> List[str]:
        return [
            f"cd {env.build_path}",
            f"{env.source_path}/configure --prefix={env.install_path}",
        ]

    def build(self, env: EnvVars) -> List[str]:
        return [f"make -C {env.build_path} -j {env.nprocs}"]

    def install(self, env: EnvVars) -> List[str]:
        return [f"make -C {env.build_path} prefix={env.install_path} install"]


class CMakeBluePrint(BluePrint):
    required_lmod = ["cmake"]

    def configure(self, env: EnvVars) -> List[str]:
        return [
            f'cmake -G"{env.cmake_build_tool}" -B ${env.build_path} -DCMAKE_INSTALL_PREFIX=${env.install_path} ${env.source_path}'
        ]

    def build(self, env: EnvVars) -> List[str]:
        return [f"cmake --build {env.build_path} -j {env.nprocs}"]

    def install(self, env: EnvVars) -> List[str]:
        return [f"cmake --install {env.build_path}"]
