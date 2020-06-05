#! /bin/bash

if [[ ! -v SRC_PATH ]] && [[ ! -v ENV_PATH ]]; then
    echo "ERROR: SRC_PATH and ENV_PATH is not defined"
    exit
fi

cd $SRC_PATH
ml cmake

if [ ! -f "ninja" ]; then
    git clone https://github.com/ninja-build/ninja.git
fi

cd ninja
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$ENV_PATH ..
make -j8
make install
