local env_path = os.getenv("ENV_PATH")
local version  = myModuleVersion()
local pkgName  = myModuleName()
pkgName = pkgName:sub(1, -2) -- Trim off the d at the end 
local pkg_path = pathJoin(env_path,pkgName,version)

-- local intel_root = os.getenv("INTEL_ROOT")
-- if (intel_root) then
--     append_path("CPATH", pathJoin(intel_root, "compiler/include"))
-- end
prepend_path("PATH", pathJoin(pkg_path, "bin"))