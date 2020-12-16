#! /bin/bash

if [[ ! -v BUILD_PATH ]] && [[ ! -v ENV_PATH ]]; then
    echo "ERROR: SRC_PATH and ENV_PATH is not defined"
    exit
fi

VERSION=2.29.2
INSTALL_PATH=$ENV_PATH/git/$VERSION

mkdir -p $BUILD_PATH
cd $BUILD_PATH

if [ ! -d "git" ]; then
    git clone --branch v$VERSION https://github.com/git/git.git
fi

cd git
make prefix=$INSTALL_PATH -j8
make prefix=$INSTALL_PATH install

if [ -v USER_MODFILES ]; then
    MF_PATH="$USER_MODFILES/git"
    mkdir -p $MF_PATH
    ln -s $BUILD_SCRIPTS/modfiles/git.lua $MF_PATH/$VERSION.lua
fi