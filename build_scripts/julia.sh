#! /bin/bash

if [[ ! -v SRC_PATH ]] && [[ ! -v ENV_PATH ]]; then
    echo "ERROR: SRC_PATH and ENV_PATH is not defined"
    exit
fi

cd $SRC_PATH

if [ ! -f "julia-1.4.2" ]; then
    wget https://julialang-s3.julialang.org/bin/linux/x64/1.4/julia-1.4.2-linux-x86_64.tar.gz
    tar -xvf julia-1.4.2-linux-x86_64.tar.gz
    rm julia-1.4.2-linux-x86_64.tar.gz
fi

rm -rf $ENV_PATH/bin/julia
ln -s $SRC_PATH/julia-1.4.2/bin/julia $ENV_PATH/bin/julia