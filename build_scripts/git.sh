#! /bin/bash

if [[ ! -v SRC_PATH ]] && [[ ! -v ENV_PATH ]]; then
    echo "ERROR: SRC_PATH and ENV_PATH is not defined"
    exit
fi

cd $SRC_PATH

if [ ! -f "git" ]; then
    git clone https://github.com/git/git.git
fi

cd git
make prefix=$ENV_PATH -j8
make prefix=$ENV_PATH install