# CBEC Workstation Bootstrap

## Quickstart

To compile QChem on the workstations in the office, just clone this repository into your home directory and run:

``` sh
bash ~/CBECws_bootstrap/build_qchem.sh 
```

and wait...

QChem will be installed into "/var/home/scratch/$USER/env/bin" from its build directory in "/var/home/scratch/$USER/env/src/qchem"

You can add this to your path by putting this code into your "~/bashrc" file:

```sh
# ... 

# Load bootstrapped environment
source $HOME/CBECws_bootstrap/load_env.sh

# Setup QCHEM
export QC=$SRC_PATH/src/qchem
export QCAUX=$SRC_PATH/src/qcaux
export QCSCRATCH=$SRC_PATH/tmp/qchem
export QCRSH=ssh
export QCMPI=openmpi
export PATH=$PATH:$QC/bin:$QC/bin/perl
```

## Development Environment

For convenience, I would recommend setting up access through the ASC SSH Jump server so you don't have to VPN in. (https://osuasc.teamdynamix.com/TDClient/1929/Portal/KB/ArticleDet?ID=29849)

I would also suggest using VSCode with the 'Remote-SSH' plugin and the `clangd` autocomplete plugin instead of VSCode's Intelisense. This will require some additional setup.
