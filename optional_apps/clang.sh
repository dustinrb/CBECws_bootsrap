#! /bin/bash

cd ~/src
ml cmake gcc/7.3
export PATH=$ENV_PATH/bin:$PATH
ninja
git clone https://github.com/llvm/llvm-project.git
cd llvm-project
mkdir -p build
cd build 
cmake -GNinja -DCMAKE_INSTALL_PREFIX=$ENV_PATH -DLLVM_ENABLE_PROJECTS='clang;clang-tools-extra' -DCMAKE_BUILD_TYPE=Release ../llvm
ninja -j8
ninja install