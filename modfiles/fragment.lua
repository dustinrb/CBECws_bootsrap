local env_path = os.getenv("ENV_PATH")
local scratch_path = os.getenv("SCRATCH_PATH")
local version  = myModuleVersion()
local pkgName  = myModuleName()
local pkg_path = pathJoin(env_path,pkgName,version)

prereq("qchem", "intel", "mkl")
prereq_any("openmpi", "mvapich", "mvapich2")

prepend_path("PATH", pathJoin(pkg_path, "bin"))
