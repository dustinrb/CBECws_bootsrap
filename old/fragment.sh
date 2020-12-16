#! /bin/bash
set -e

# THESE VARIABLES CAN BE SETUP BY RUNNING the scripts in the `env`
if [[ ! -v SRC_PATH ]] && [[ ! -v ENV_PATH ]]; then
  echo "ERROR: SRC_PATH and ENV_PATH is not defined"
  exit
fi

VERSION="master"

FRAG_SRC_PATH=$SRC_PATH/fragment/$VERSION
FRAG_BUILD_PATH=$BUILD_PATH/fragment/$VERSION
FRAG_INSTALL_PATH=$ENV_PATH/fragment/$VERSION

if [ ! -d $FRAG_SRC_PATH ]; then
  # Get source
  git clone --branch $VERSION git@gitlab.com:forthehorde/fragment.git $FRAG_SRC_PATH
fi


mkdir -p $FRAG_BUILD_PATH
cd $FRAG_BUILD_PATH

CC=mpicc CXX=mpic++ LD=mpic++ cmake \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=YES \
  -DCMAKE_INSTALL_PREFIX=$FRAG_INSTALL_PATH \
  $FRAG_SRC_PATH

cmake --build . -- -j 8 # Build with 8 threads
cmake --install .

if [ -v USER_MODFILES ]; then
    MF_PATH="$USER_MODFILES/fragment"
    mkdir -p $MF_PATH
    ln -s $BUILD_SCRIPTS/modfiles/fragment.lua $MF_PATH/$VERSION.lua
fi