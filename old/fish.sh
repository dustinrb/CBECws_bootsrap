#! /bin/bash

if [[ ! -v BUILD_PATH ]] && [[ ! -v ENV_PATH ]]; then
    echo "ERROR: SRC_PATH and ENV_PATH is not defined"
    exit
fi

VERSION=3.1.2
INSTALL_PATH=$ENV_PATH/fish/$VERSION

mkdir -p $BUILD_PATH
cd $BUILD_PATH

if [ ! -d "fish-shell" ]; then
    git clone --branch $VERSION https://github.com/fish-shell/fish-shell.git
fi

cd fish-shell
mkdir -p build
cd build
CC=gcc CXX=g++ cmake -GNinja -DCMAKE_INSTALL_PREFIX=$INSTALL_PATH ..
cmake --build . -- -j8
cmake --install . 

# INSTALL BASS
if [ ! -f "$HOME/.config/fish/functions/fisher.fish" ]; then
    curl https://git.io/fisher --create-dirs -sLo ~/.config/fish/functions/fisher.fish
    fisher add edc/bass
fi

if [ -v USER_MODFILES ]; then
    MF_PATH="$USER_MODFILES/fish"
    mkdir -p $MF_PATH
    ln -s $BUILD_SCRIPTS/modfiles/fish.lua $MF_PATH/$VERSION.lua
fi