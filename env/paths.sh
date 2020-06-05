# SETUP PATHS
export SCRATCH_PATH=/var/home/scratch/$ENV_PATH
export ENV_PATH=$SCRATCH_PATH/env
export SRC_PATH=$ENV_PATH/src

# ENV_PATH will the the working directory for our scripts
mkdir -p SRC_PATH

# LINK THE ENV PATH TO $HOME FOR CONVENIENCE
if [ ! -h $src_target ]; then
    ln -s $ENV_PATH $HOME/src
fi

# SET PATH VARIABLES TO USE OUR ENV
export LIBRARY_PATH=$ENV_PATH/lib64:$ENV_PATH/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=$ENV_PATH/lib64:$ENV_PATH/lib:$LD_LIBRARY_PATH
export CPATH=$ENV_PATH/include:$CPATH
export PATH=$ENV_PATH/bin:$PATH