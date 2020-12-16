#! /bin/bash
source $TOOLCHAIN_PATH/load.sh devel

# THESE VARIABLES CAN BE SETUP BY RUNNING the scripts in the `env`
if [[ ! -v SRC_PATH ]] && [[ ! -v ENV_PATH ]]; then
  echo "ERROR: SRC_PATH and ENV_PATH is not defined"
  exit
fi

cd $SRC_PATH

if [ ! -d "libint-2.6.0" ]; then
  # Get source
  wget https://github.com/evaleev/libint/releases/download/v2.6.0/libint-2.6.0.tgz
  tar xzvf libint-2.6.0.tgz
  rm -rf libint-2.6.0.tgz
fi

cd libint-2.6.0
./configure --prefix=$ENV_PATH --enable-fortran --with-cxx-optflags='-O2'
make -j8
make install

# SET INSTALL DIRECTORY AND CREATE compile_commands.js FOR clangd
