# SET COMPILER VARIABLES
export LD=ifort
export CC=icc
export CXX=icpc
export FC=ifort

# MAKE ifort COMPATIBLE WITH OLD STANDARDS
export F77=ifort
export F77FLAGS="-f77rtl $F77FLAGS"
export F90=ifort
export F90FLAGS="-stand f90 $F90FLAGS"

# USE OPTIMIZATION FLAGS
export CFLAGS="-march=native -mtune=native"
export CXXFLAGS="-march=native -mtune=native"
export FFLAGS="-march=native -mtune=native"

# PREVENTS BUGS WHEN COMPILING OLD FORTRAN CODE
export LDFLAGS="-nofor_main"
