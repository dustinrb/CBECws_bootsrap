local env_path = os.getenv("ENV_PATH")
local version  = myModuleVersion()
local pkgName  = myModuleName()
local pkg_path = pathJoin(env_path,pkgName,pkgName .. "-" .. version .. "-Linux-x86_64")

prepend_path("PATH", pathJoin(pkg_path, "bin"))
prepend_path("MANPATH", pathJoin(pkg_path, "man"))