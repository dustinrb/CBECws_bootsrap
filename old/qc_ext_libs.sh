#! /bin/bash
source $TOOLCHAIN_PATH/load.sh devel

# THESE VARIABLES CAN BE SETUP BY RUNNING the scripts in the `env`
if [[ ! -v SRC_PATH ]] && [[ ! -v ENV_PATH ]] && [[ ! -v QC_EXT_LIBS ]]; then
  echo "ERROR: SRC_PATH and ENV_PATH is not defined"
  exit
fi

if [ ! -f "$SRC_PATH/libcosmo2_linux64_ifort16.a" ]; then 
  cosmos2_path=$QC_EXT_LIBS/libcosmo2/lib
  mkdir -p $cosmos2_path
  cp $SRC_PATH/libcosmo2_linux64_ifort16.a $cosmos2_path
fi

intracule_path=$QC_EXT_LIBS/libintracule
mkdir -p $intracule_path

cd $SRC_PATH
if [ ! -d "libintracule-src" ]; then
  # Get source
  svn co https://jubilee.q-chem.com/svnroot/libintracule/trunk libintracule-src
fi

cd libintracule-src
./configure --prefix=$intracule_path --toolchain=intel --build=release
cd build
make -j8 install

if [ ! -d "fftw-2.1.5" ]; then
  # Get source
  wget http://www.fftw.org/fftw-2.1.5.tar.gz
  tar xzf fftw-2.1.5.tar.gz
  rm -rf fftw-2.1.5.tar.gz
fi

cd fftw-2.1.5

# DO ACTUAL BUILD
./configure CC=icc F77=ifort --prefix=$QC_EXT_LIBS/fftw --enable-shared --enable-mpi
make all install
