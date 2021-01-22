local env_path = os.getenv("ENV_PATH")
local version  = myModuleVersion()
local pkgName  = myModuleName()
local pkg_path = pathJoin(env_path, pkgName, version)

pushenv("EFP_FRAGLIB", pathJoin(pkg_path, "share", "libefp", "fraglib"))

prepend_path("LIBRARY_PATH", pathJoin(pkg_path, "lib64"))
prepend_path("LD_LIBRARY_PATH", pathJoin(pkg_path, "lib64"))
prepend_path("CPATH", pathJoin(pkg_path, "include"))
prepend_path("CMAKE_PREFIX_PATH", pathJoin(pkg_path, "share", "cmake", "libefp"))
