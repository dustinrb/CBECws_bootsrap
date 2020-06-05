#! /bin/bash

if [[ ! -v SRC_PATH ]] && [[ ! -v ENV_PATH ]]; then
    echo "ERROR: SRC_PATH and ENV_PATH is not defined"
    exit
fi

cd $SRC_PATH

if [ ! -d "fish-shell" ]; then
    git clone https://github.com/fish-shell/fish-shell.git
fi

cd fish-shell
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$ENV_PATH ..
make -j8
make install

# INSTALL BASS
if [ ! -f "$HOME/.config/fish/functions/fisher.fish" ]; then
    curl https://git.io/fisher --create-dirs -sLo ~/.config/fish/functions/fisher.fish
    fisher add edc/bass
fi