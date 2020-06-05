# SET VERSION INFORMATION
intel_version="18.2"
mkl_version="17.1"
python_version="3.7"
mpi_flavor="openmpi"
mpi_version="2.0"
boost_version="1.67"

# IMPORT THE MODULES
module load intel/$intel_version $mpi_flavor/$mpi_version
module load \
    mkl/$mkl_version
    python/$python_version \
    boost/$boost_version \
    cmake