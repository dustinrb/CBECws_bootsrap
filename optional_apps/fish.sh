#! /bin/bash

cd ~/src
ml cmake
git clone https://github.com/fish-shell/fish-shell.git
cd fish-shell
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$ENV_PATH ..
make -j8
make install