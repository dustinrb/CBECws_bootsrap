#! /bin/bash

if [[ ! -v SRC_PATH ]] && [[ ! -v ENV_PATH ]]; then
    echo "ERROR: SRC_PATH and ENV_PATH is not defined"
    exit
fi

cd $SRC_PATH
VERSION="1.10.2"

if [ ! -d "ninja" ]; then
    wget https://github.com/ninja-build/ninja/releases/download/v$VERSION/ninja-linux.zip
    unzip ninja-linux.zip
    mkdir -p $ENV_PATH/ninja/$VERSION/bin
    mv ninja $ENV_PATH/ninja/$VERSION/bin
fi

if [ -v USER_MODFILES ]; then
    MF_PATH="$USER_MODFILES/ninja"
    mkdir -p $MF_PATH
    ln -s $BUILD_SCRIPTS/modfiles/ninja.lua $MF_PATH/$VERSION.lua
fi