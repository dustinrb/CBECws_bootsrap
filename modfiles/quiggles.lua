local env_path = os.getenv("BUILD_SCRIPTS")

local bin_path = pathJoin(env_path, "bin")
prepend_path("PATH", bin_path)