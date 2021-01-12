local env_path = os.getenv("ENV_PATH")
local version  = myModuleVersion()
local pkgName  = myModuleName()
local pkg_path = pathJoin(env_path,pkgName,version)

load("eigen", "boost")

prepend_path("LIBRARY_PATH", pathJoin(pkg_path, "lib"))
prepend_path("LD_LIBRARY_PATH", pathJoin(pkg_path, "lib"))
prepend_path("CPATH", pathJoin(pkg_path, "include"))
