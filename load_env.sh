# Change to this script's location
old_path=`pwd`

cd `dirname ${BASH_SOURCE[0]}`
# cd `dirname $0`

source ./env/paths.sh   # Paths for the workstation
source ./env/modules.sh # Required modules
source ./env/dev.sh     # Compiler variabls

cd $old_path
