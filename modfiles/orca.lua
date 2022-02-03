local env_path = os.getenv("ENV_PATH")
local version  = myModuleVersion()
local pkgName  = myModuleName()
local pkg_path = pathJoin(env_path,pkgName,version)

prepend_path("PATH", pkg_path)
prepend_path("LD_LIBRARY_PATH", pkg_path)
