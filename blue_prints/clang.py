from typing import List

from brick_yard.blue_print import CMakeBluePrint, EnvVars


class clang(CMakeBluePrint):
    """
    clangd -- Used for vscode clangd completion on CBEC computers
    """

    name = "clang"
    version = "13.0.1"
    required_lmod = ["cmake", "gcc"]

    def source(self, env: EnvVars) -> List[str]:
        return [
            f"git clone --branch llvmorg-{env.version} https://github.com/llvm/llvm-project.git {env.source_path}"
        ]

    def configure(self, env: EnvVars) -> List[str]:
        return [
            # f"CC=gcc CXX=g++ "
            f'"cmake -G"{env.cmake_build_tool}"'
            f" -B {env.build_path}"
            f" -DCMAKE_INSTALL_PREFIX={env.install_path}"
            # f" -DCMAKE_CXX_LINK_FLAGS=-Wl,-rpath,/opt/modules/gcc/7.3/lib64 -L/opt/modules/gcc/7.3/lib64"
            f" -DLLVM_ENABLE_PROJECTS='clang;clang-tools-extra;libcxx;libcxxabi;openmp;parallel-libs;'"
            f' -DLLVM_TARGETS_TO_BUILD="X86"'
            f" -DCMAKE_BUILD_TYPE=Release"
            f" -DLLVM_BUILD_EXAMPLES=OFF"
            f" -DLLVM_INCLUDE_EXAMPLES=OFF"
            f" -DLLVM_BUILD_TESTS=OFF"
            f" -DLLVM_INCLUDE_TESTS=OFF"
            f" -DLLVM_INCLUDE_BENCHMARKS=OFF"
            f" -DLLVM_TEMPORARILY_ALLOW_OLD_TOOLCHAIN=YES"
            f" {env.source_path}/llvm"
        ]
