local env_path = "/opt/modules/gcc"
local version  = myModuleVersion()
local pkg_path = pathJoin(env_path, version)

family("compatibility")
-- prepend_path("PATH", pathJoin(pkg_path, "bin"))
prepend_path("LD_LIBRARY_PATH", pathJoin(pkg_path, "lib"))
prepend_path("LD_LIBRARY_PATH", pathJoin(pkg_path, "lib64"))
-- prepend_path("LIBRARY_PATH", pathJoin(pkg_path, "lib"))
-- prepend_path("LIBRARY_PATH", pathJoin(pkg_path, "lib64"))
-- prepend_path("CPATH", pathJoin(pkg_path, "include"))