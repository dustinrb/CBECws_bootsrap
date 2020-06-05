#! /bin/bash

cd ~/src
wget https://julialang-s3.julialang.org/bin/linux/x64/1.4/julia-1.4.2-linux-x86_64.tar.gz
tar -xvf julia-1.4.2-linux-x86_64.tar.gz
rm julia-1.4.2-linux-x86_64.tar.gz
ln -s ~/src/julia-1.4.2/bin/julia $ENV_PATH/bin/julia