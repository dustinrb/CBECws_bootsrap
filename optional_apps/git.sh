#! /bin/bash

cd $HOME/src
git clone https://github.com/git/git.git
cd git
make prefix=$ENV_PATH -j8
make prefix=$ENV_PATH install