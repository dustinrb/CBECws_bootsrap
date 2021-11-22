local env_path = os.getenv("ENV_PATH")
local version = myModuleVersion()
local pkgName = myModuleName()
local pkg     = pathJoin(env_path,pkgName,version,"bin")

prepend_path("PATH", pkg)
pushenv("MOPAC_LICENSE", pkg)