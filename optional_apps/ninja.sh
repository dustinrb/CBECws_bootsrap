#! /bin/bash

cd ~/src
ml cmake
git clone https://github.com/ninja-build/ninja.git
cd ninja
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$ENV_PATH ..
make -j8
make install
