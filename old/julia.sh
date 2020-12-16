#! /bin/bash

if [[ ! -v SRC_PATH ]] && [[ ! -v ENV_PATH ]]; then
    echo "ERROR: SRC_PATH and ENV_PATH is not defined"
    exit
fi

cd $SRC_PATH
VERSION="1.5.2"
SHORT_VERSION="1.5"

if [ ! -d "julia-$VERSION" ]; then
    wget https://julialang-s3.julialang.org/bin/linux/x64/$SHORT_VERSION/julia-$VERSION-linux-x86_64.tar.gz
    mkdir -p $ENV_PATH/julia
    tar -xf julia-$VERSION-linux-x86_64.tar.gz -C $ENV_PATH/julia/
    rm julia-$VERSION-linux-x86_64.tar.gz
fi

rm -rf $ENV_PATH/bin/julia

if [ -v USER_MODFILES ]; then
    MF_PATH="$USER_MODFILES/julia"
    mkdir -p $MF_PATH
    ln -s $BUILD_SCRIPTS/modfiles/julia.lua $MF_PATH/$VERSION.lua
fi
