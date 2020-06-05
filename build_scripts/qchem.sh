#! /bin/bash

# THESE VARIABLES CAN BE SETUP BY RUNNING the scripts in the `env`
if [[ ! -v SRC_PATH ]] && [[ ! -v ENV_PATH ]]; then
  echo "ERROR: SRC_PATH and ENV_PATH is not defined"
  exit
fi

cd $SRC_PATH

if [ ! -d "qchem" ]; then
  # Get source
  svn co https://jubilee.q-chem.com/svnroot/qchem/trunk qchem
fi

if [ ! -d "qcaux" ]; then
  # Setup qcaux while we are here
  svn co https://jubilee.q-chem.com/svnroot/qcaux/trunk qcaux
  cd qcaux
  wget http://www.q-chem.com/download/qc_latest/drivers/drivers.small.tar.gz
  tar xzf drivers.small.tar.gz
  cd $SRC_PATH
fi

cd qchem

# USE ninja IF AVAILABLE
if [ -x "$(command -v ninja)" ]; then
  BUILD_TOOL=ninja
fi

# DO ACTUAL BUILD
if [ ! -d "build" ]; then
  ./configure intel mkl openmp relwdeb nointracule nomgc nodmrg noccman2 $BUILD_TOOL
fi
cd build

# SET INSTALL DIRECTORY AND CREATE compile_commands.js FOR clangd
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=YES -DCMAKE_INSTALL_PREFIX=$ENV_PATH ..
cmake --build . -- -j 8 # Build with 8 threads
cmake --install .
