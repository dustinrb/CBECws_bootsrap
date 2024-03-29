local env_path = os.getenv("ENV_PATH")
local scratch_path = os.getenv("SCRATCH_PATH")
local version  = myModuleVersion()
local pkgName  = myModuleName()
local pkg_path = pathJoin(env_path,pkgName,version)

load("qcaux")
try_load("qchem_dailyref")

prepend_path("PATH", pathJoin(pkg_path, "bin"))
pushenv("QC", pkg_path)
pushenv("QCSCRATCH", pathJoin(scratch_path, "tmp", "qchem"))
setenv("QCRSH", "ssh")
setenv("QCPLATFORM", "LINUX_Ix86_64")
