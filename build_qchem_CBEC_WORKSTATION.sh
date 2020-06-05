#! /bin/bash

# PATHS
# Setup our build build paths
export SCRATCH_PATH=/var/home/scratch/$USER
export ENV_PATH=$SCRATCH_PATH/env
export SRC_PATH=$SCRATCH_PATH/src
export TMP_PATH=$SCRATCH_PATH/tmp

mkdir -p $ENV_PATH
mkdir -p $SRC_PATH
mkdir -p $TMP_PATH

# VERSIONS
# Set Version numbers and import needed modules
intel_version="18.2"
mkl_version="17.1"
python_version="3.7"

mpi_flavor="openmpi"
mpi_version="2.0"

boost_version="1.67"

# Load our dependencies
module load \
  intel/$intel_version \
  $mpi_flavor/$mpi_version \
  python/$python_version \
  boost/$boost_version \
  cmake \
  > /dev/null

# BUILD VARIABLES
# Export our clobal variables
export LD=ifort
export CC=icc
export CXX=icpc
export FC=ifort
export F77=ifort
export F77FLAGS="-f77rtl $F77FLAGS"
export F90=ifort
export F90FLAGS="-stand f90 $F90FLAGS"
export CFLAGS="-march=native -mtune=native"
export CXXFLAGS="-march=native -mtune=native"
export FFLAGS="-march=native -mtune=native"
export LDFLAGS="-nofor_main"

