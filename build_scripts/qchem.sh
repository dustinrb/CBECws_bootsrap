#! /bin/bash

# THESE VARIABLES CAN BE SETUP BY RUNNING the scripts in the `env`
if [[ ! -v SRC_PATH ]] && [[ ! -v ENV_PATH ]]; then
  echo "ERROR: SRC_PATH and ENV_PATH is not defined"
  exit
fi

cd $SRC_PATH

if [ ! -f "qchem" ] && [ ! -f "qcaux" ]; then
  # Get source
  svn co https://jubilee.q-chem.com/svnroot/qchem/trunk qchem

  # Setup qcaux while we are here
  svn co https://jubilee.q-chem.com/svnroot/qcaux/trunk qcaux
  cd qcaux
  wget http://www.q-chem.com/download/qc_latest/drivers/drivers.small.tar.gz
  tar xzf drivers.small.tar.gz
  cd $SRC_PATH
fi

# PICK BETWEEN NINJA OR MAKE
BUILD_TOOL = make
# Prefere ninja if available (SEE build_scripts/ninja.sh script)
if [ -x "$(command -v ninja)" ]; then
  BUILD_TOOL = ninja
fi

# DO ACTUAL BUILD
./configure intel mkl openmp relwdeb nointracule nomgc nodmrg noccman2 $BUILD_TOOL
cd build

# SET INSTALL DIRECTORY AND CREATE compile_commands.js FOR clangd
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=YES -DCMAKE_INSTALL_PREFIX=$ENV_PATH ..
cd cmake --build . -- -j 8 # Build with 8 threads
