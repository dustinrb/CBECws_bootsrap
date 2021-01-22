local env_path = os.getenv("ENV_PATH")
local version  = myModuleVersion()
local pkgName  = myModuleName()
local pkg_path = pathJoin(env_path,pkgName,version)

local intel_root = os.getenv("INTEL_ROOT")
-- if (intel_root) then
--     append_path("CPATH", pathJoin(intel_root, "compiler/include"))
-- end
prepend_path("PATH", pathJoin(pkg_path, "bin"))
prepend_path("MANPATH", pathJoin(pkg_path, "share", "man"))