#! /bin/bash

if [[ ! -v BUILD_PATH ]] && [[ ! -v ENV_PATH ]]; then
    echo "ERROR: SRC_PATH and ENV_PATH is not defined"
    exit
fi

VERSION=11.0.0
INSTALL_PATH=$ENV_PATH/clangd/$VERSION

mkdir -p $BUILD_PATH
cd $BUILD_PATH

if [ ! -d "llvm-project" ]; then
    git clone --branch llbmorg-$VERSION https://github.com/llvm/llvm-project.git
fi

# Get a recent version of gcc
ml gcc

cd llvm-project
mkdir -p build
cd build 
CC=gcc CXX=g++ cmake -GNinja \
    -DCMAKE_INSTALL_PREFIX=$INSTALL_PATH \
    -DLLVM_ENABLE_PROJECTS='clang;clang-tools-extra' \
    -DLLVM_TARGETS_TO_BUILD="X86" \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_BUILD_EXAMPLES=OFF \
    -DLLVM_INCLUDE_EXAMPLES=OFF \
    -DLLVM_BUILD_TESTS=OFF \
    -DLLVM_INCLUDE_TESTS=OFF \
    -DLLVM_INCLUDE_BENCHMARKS=OFF \
    ../llvm
ninja -j8
ninja install

if [ -v USER_MODFILES ]; then
    MF_PATH="$USER_MODFILES/clangd"
    mkdir -p $MF_PATH
    ln -s $BUILD_SCRIPTS/modfiles/clangd.lua $MF_PATH/$VERSION.lua
fi