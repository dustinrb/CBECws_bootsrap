#! /bin/bash

if [[ ! -v SRC_PATH ]] && [[ ! -v ENV_PATH ]]; then
    echo "ERROR: SRC_PATH and ENV_PATH is not defined"
    exit
fi

cd $SRC_PATH
ml gcc/7.3
export PATH=$ENV_PATH/bin:$PATH

if [ ! -d "llvm-project" ]; then
    git clone https://github.com/llvm/llvm-project.git
fi

cd llvm-project
mkdir -p build
cd build 
cmake -GNinja -DCMAKE_INSTALL_PREFIX=$ENV_PATH -DLLVM_ENABLE_PROJECTS='clang;clang-tools-extra' -DCMAKE_BUILD_TYPE=Release ../llvm
ninja -j8
ninja install