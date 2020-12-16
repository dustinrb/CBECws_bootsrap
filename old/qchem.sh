#! /bin/bash
set -e

SVN_ROOT="https://jubilee.q-chem.com/svnroot/qchem"
BRANCH=$1
SVN_URL=$SVN_ROOT/$BRANCH
if [ -z "$BRANCH" ]; then
  echo "ERROR: Give the branch you want as an argument"
  exit 1
fi

# REQUIRED ENV VARIABLES
if [[ ! -v SRC_PATH ]] && [[ ! -v ENV_PATH ]] && [[ ! -v BUILD_PATH ]]; then
  echo "ERROR: SRC_PATH, ENV_PATH, and BUILD_PATH are not defined"
  exit 1
fi

QCNAME=`basename $BRANCH`
QCSRC=$SRC_PATH/qchem
BRANCH_SRC=$QCSRC/$QCNAME
QCINSTALL=$ENV_PATH/qchem/$QCNAME
QCBUILD_abs=$BUILD_PATH/qchem/$QCNAME

echo "THE FOLLOWING WILL BE TRUE ONCE THIS SCRIPT RUNS:"
echo "  SVN WILL CHECKOUT: $SVN_URL"
echo "  SOURCE CODE IN:    $BRANCH_SRC"
echo "  INSTALLED IN:      $QCINSTALL"
echo "  BUILD FILES IN:    $QCBUILD_abs"
# read -p "Press ENTER to continue (CTL C to stop)..."

mkdir -p $QCSRC

# Dirty hack to get an out-of-source build

if [ ! -d "$BRANCH_SRC" ]; then
  svn co $SVN_URL $BRANCH_SRC
fi

QCBUILD=`realpath --relative-to=$BRANCH_SRC $QCBUILD_abs`

# DO ACTUAL BUILD
if [ ! -d $QCBUILD_abs ] || [ -z "$(ls -A $QCBUILD_abs)" ]; then
  mkdir -p $QCBUILD_abs
  cd $BRANCH_SRC

  QCBUILD=$QCBUILD ./configure intel mkl openmp relwdeb nointracule nomgc nodmrg noccman2 --prefix=$QCINSTALL
  cd $QCBUILD_abs
  cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=YES $BRANCH_SRC
fi

# DO BUILD
CPUS=8
[ -v SLURM_NTASKS ] && CPUS=$SLURM_NTASKS

cd $QCBUILD_abs
cmake --build . -- -j $CPUS # Build with 8 threads
cmake --install .
sed  -i 's/-qopenmp/-fopenmp/g' $QCBUILD_abs/compile_commands.json
if [ ! -e $BRANCH_SRC/compile_commands.json ]; then
  ln -s $QCBUILD_abs/compile_commands.json $BRANCH_SRC/
fi

VERSION=$QCNAME
if [ -v USER_MODFILES ]; then
    MF_PATH="$USER_MODFILES/qchem"
    mkdir -p $MF_PATH
    ln -s $BUILD_SCRIPTS/modfiles/qchem.lua $MF_PATH/$VERSION.lua
fi
