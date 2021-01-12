local src_path = os.getenv("BUILD_PATH")
local scratch_path = os.getenv("SCRATCH_PATH")

local version  = myModuleVersion()
local pkgName  = myModuleName()
local qc_path = pathJoin(src_path, "qchem", version)

load("qcaux", "qchem_dailyref")

pushenv("QC", qc_path)
pushenv("QCEXE", pathJoin(qc_path, "qcprog.exe"))
pushenv("QCSCRATCH", pathJoin(scratch_path, "tmp", "qchem"))
setenv("QCRSH", "ssh")
setenv("QCPLATFORM", "LINUX_Ix86_64")
