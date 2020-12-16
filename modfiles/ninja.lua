local env_path = os.getenv("ENV_PATH")
local version = myModuleVersion()
local pkgName = myModuleName()
local pkg     = pathJoin(env_path,pkgName,version,"bin")

family("build_tool")

prepend_path("PATH", pkg)