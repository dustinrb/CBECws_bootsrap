#! /bin/bash

cd `dirname ${BASH_SOURCE[0]}`

source ./load_env.sh

for app in `ls build_scripts`; do
    echo "RUNNING ./build_scripts/$app"
    bash ./build_scripts/$app
done

echo "INSTALLATION DONE!"