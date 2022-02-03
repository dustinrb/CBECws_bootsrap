import json
from copy import copy
from pathlib import Path
from typing import Dict, List

from tasks.build.BuildJob import BuildJob
from tasks.build.BuildRunner import BashRunner, PrintRunner
from tasks.build.LMod import is_loaded


@build_task
def armadillo(ctx, version="10.2.x"):
    """
    C++ matrix library in headers
    """
    return BuildJob(
        "armadillo",
        version,
        source_cmd="git clone --branch {env.version} https://gitlab.com/conradsnicta/armadillo-code.git {env.source_path}",
    )


@build_task
def clang(ctx, version="11.0.1"):
    """
    clangd -- Used for vscode clangd completion on CBEC computers
    """
    return BuildJob(
        "clang",
        version,
        required_build_pkgs=["cmake", "gcc"],
        source_cmd="git clone --branch llvmorg-{env.version} https://github.com/llvm/llvm-project.git {env.source_path}",
        configure_cmd=[
            'CC=gcc CXX=g++ cmake -G"{env.cmake_build_tool}" '
            "-B {env.build_path} "
            "-DCMAKE_INSTALL_PREFIX={env.install_path} "
            "-DCMAKE_CXX_LINK_FLAGS=-Wl,-rpath,/opt/modules/gcc/7.3/lib64 -L/opt/modules/gcc/7.3/lib64 "
            "-DLLVM_ENABLE_PROJECTS='clang;clang-tools-extra;libcxx;libcxxabi;openmp;parallel-libs;' "
            '-DLLVM_TARGETS_TO_BUILD="X86" '
            "-DCMAKE_BUILD_TYPE=Release "
            "-DLLVM_BUILD_EXAMPLES=OFF "
            "-DLLVM_INCLUDE_EXAMPLES=OFF "
            "-DLLVM_BUILD_TESTS=OFF "
            "-DLLVM_INCLUDE_TESTS=OFF "
            "-DLLVM_INCLUDE_BENCHMARKS=OFF "
            "-DLLVM_TEMPORARILY_ALLOW_OLD_TOOLCHAIN=YES "
            "{env.source_path}/llvm "
        ],
        build_cmd="cmake --build . -j {env.nprocs}",
        install_cmd="cmake --install {env.build_path}",
    )

    # TODO: Create mathod for adding clangd wrapper


@build_task
def eigen(ctx, version="3.3.9"):
    """
    eigen -- Header library for matrix operations
    """
    return BuildJob(
        "eigen",
        version,
        required_build_pkgs=["cmake"],
        source_cmd="git clone --branch {env.version} https://gitlab.com/libeigen/eigen.git {env.source_path}",
    )


@build_task
def fish(ctx, version="3.3.1"):
    """
    fish -- Shell that is vastly better than bash
    """
    return BuildJob(
        "fish",
        version,
        required_build_pkgs=["cmake", "intel"],
        source_cmd="git clone --branch {env.version} https://github.com/fish-shell/fish-shell.git {env.source_path}",
        configure_cmd='CC=gcc CXX=g++ cmake -B {env.build_path} -G"{env.cmake_build_tool}" -DCMAKE_INSTALL_PREFIX={env.install_path} {env.source_path}',
    )


@build_task
def fragment(ctx, version="master"):
    """
    fragment -- Original verion of fragment. For legacy
    """
    return BuildJob(
        "fragment",
        version,
        required_build_pkgs=["cmake"],
        required_pkgs=["intel", "mpi"],
        source_cmd="git clone git@gitlab.com:forthehorde/fragment.git {env.source_path}",
        configure_cmd="CC=mpicc CXX=mpic++ LD=mpic++ cmake -B {env.build_path} -DCMAKE_INSTALL_PREFIX={env.install_path} -DCMAKE_EXPORT_COMPILE_COMMANDS=yes {env.source_path}",
        build_cmd=[
            "cmake --build {env.build_path} -- -j {env.nprocs}",
            "sed  -i 's/-qopenmp/-fopenmp/g' {env.build_path}/compile_commands.json",
            "ln -s {env.build_path}/compile_commands.json {env.source_path}/",
        ],
    )


@build_task
def hdf5(ctx, version="1.12.1"):
    """
    HDF5 library needed for QChem
    """
    short_version = version[0 : version.rfind(".")]

    # https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.1/src/CMake-hdf5-1.12.1.tar.gz
    # base_folder = "CMake-hdf5-{version}".format(version=version)

    # https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.1/src/hdf5-1.12.1.tar.gz
    base_folder = "hdf5-{version}".format(version=version)

    tar_file = "{}.tar.gz".format(base_folder)
    url = f"https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-{short_version}/hdf5-{version}/src/{tar_file}"

    return BuildJob(
        "hdf5",
        version,
        required_build_pkgs=["cmake", "ninja"],
        required_pkgs=["intel"],
        source_cmd=[
            "wget {} -P {env.source_path}".format(url),
            "tar -xf {env.source_path}/{} -C {env.source_path}".format(tar_file),
            "rm -rf {env.source_path}/{}".format(tar_file),
            "mv {env.source_path}/{}/* ./".format(base_folder),
        ],
        configure_cmd=[
            "cd {env.build_path}; {env.source_path}/configure --prefix={env.install_path} --enable-fortran --enable-cxx"
        ],
        build_cmd="make -j {env.nprocs}",
        install_cmd="make install",
    )


# @build_task
# def gcc_compatibility(ctx, version="7.3"):
#     """
#     gcc_compatibility -- Makes newer GCC libs available while having Intel compilers loaded
#     """
#     return BuildJob(
#         "gcc_compatibility",
#         version,
#         source_cmd="mkdir -p {env.source_path}",
#         configure_cmd="",
#         build_cmd="",
#         install_cmd=""
#     )


@build_task
def libint(ctx, version="2.6.0"):
    """
    libint -- Integral library for QChem and CP2K
    """
    base_folder = "libint-{version}".format(version=version)
    tar_file = "{}.tgz".format(base_folder)
    url = "https://github.com/evaleev/libint/releases/download/v{version}/{tf}".format(
        version=version, tf=tar_file
    )

    return BuildJob(
        "libint",
        version,
        source_cmd=[
            "wget {} -P {env.source_path}".format(url),
            "tar -xf {env.source_path}/{} -C {env.source_path}".format(tar_file),
            "rm -rf {env.source_path}/{}".format(tar_file),
            "mv {env.source_path}/{}/* ./".format(base_folder),
        ],
    )


@build_task
def qcaux(ctx, version="trunk"):
    """
    qcaux -- basis set definitions for QChem
    """

    SVN_ROOT = "https://jubilee.q-chem.com/svnroot/qcaux"

    version = version.strip()
    if version == "trunk":
        source_url = "{}/{}".format(SVN_ROOT, version)
    else:
        source_url = "{}/branches/{}".format(SVN_ROOT, version)

    return BuildJob(
        "qcaux",
        version,
        source_cmd=[
            f"svn co {source_url} {env.install_path}",
            "wget https://downloads.q-chem.com/qcinstall/drivers/drivers.linux.tar.gz -P {env.install_path}/",
        ],
        configure_cmd="",
        build_cmd="",
        install_cmd=,
    )


@build_task
def qchem(ctx, version="trunk"):
    """
    qchem -- QChem software package. Clones from SVN
    """
    SVN_ROOT = "https://jubilee.q-chem.com/svnroot/qchem"

    # Choose the correct branching information
    version = version.strip()
    if version == "trunk":
        source_url = "{}/{}".format(SVN_ROOT, version)
    else:
        source_url = "{}/branches/{}".format(SVN_ROOT, version)

    # Provide an option to use nina (NINJA!)
    if is_loaded("ninja"):
        build_tool_flag = "ninja "
    else:
        build_tool_flag = ""

    return BuildJob(
        "qchem",
        version,
        source_cmd="svn co {} {env.source_path}".format(source_url),
        configure_cmd=[
            "QCBUILD=`realpath relative-to={env.build_path} {env.source_path}` "
            # "./configure intel mkl openmp relwdeb nointracule nomgc noccman2 "
            "./configure intel mkl openmp rel "
            "{btf} --prefix={env.install_path}".format(btf=build_tool_flag),
            "cmake -B {env.build_path} -DCMAKE_EXPORT_COMPILE_COMMANDS=YES {env.source_path}",
        ],
        build_cmd=[
            "cmake --build {env.build_path} --target qcprog.exe -- -j {env.nprocs}"
        ],
        install_cmd=[
            "mkdir -p {env.install_path}/exe",
            # Manually install qcexe
            "cp {env.build_path}/qcprog.dbg {env.install_path}/exe",
            "cp {env.build_path}/qcprog.exe {env.install_path}/exe",
            "cp -r {env.source_path}/bin {env.install_path}",
            "[[ ! -L {env.install_path}/bin/mpi ]] && ln -s {env.source_path}/bin/mpi {env.install_path}/bin/mpi",
        ],
        required_pkgs=["intel", "mkl"],
        required_build_pkgs=["cmake"],
    )


@build_task
def qchem_test(ctx, version="trunk"):
    """
    qchem_test -- dummy package which installs modfile to enable testing qchem without loading the executables
    """
    return BuildJob(
        "qchem_test",
        version,
        source_cmd="",
        configure_cmd="",
        build_cmd="",
        install_cmd="",
        required_pkgs=["intel", "mkl"],
    )


@build_task
def qchem_dailyref(ctx, version="trunk"):
    """
    qchem_dailyref -- test file reference values for qchem
    """
    SVN_ROOT = "https://jubilee.q-chem.com/svnroot/qchem_dailyref"

    # Choose the correct branching information
    version = version.strip()
    if version == "trunk":
        source_url = "{}/{}".format(SVN_ROOT, version)
    else:
        source_url = "{}/branches/{}".format(SVN_ROOT, version)

    return BuildJob(
        "qchem_dailyref",
        version,
        source_cmd="svn co {} {env.source_path}".format(source_url),
        configure_cmd="",
        build_cmd="",
        install_cmd=[
            "mkdir -p {env.ENV_PATH}/qchem_dailyref",
            "[[ ! -L {env.install_path} ]] && ln -s {env.source_path} {env.install_path}",
            "svn up {env.source_path}",
        ],
        required_pkgs=[],
        required_build_pkgs=[],
    )


@build_task
def git(ctx, version="2.29.2"):
    """
    git -- newer version of git needed for VSCode
    """
    return BuildJob(
        "git",
        version,
        source_cmd="git clone --branch v{env.version} https://github.com/git/git.git {env.source_path}",
        configure_cmd="",
        build_cmd="make -C {env.source_path} prefix={env.install_path} -j {env.nprocs}",
        install_cmd="make -C {env.source_path} prefix={env.install_path} install",
    )


@build_task
def julia(ctx, version="1.5.3"):
    """
    julia -- Julia programming language
    """
    v_parts = version.split(".")
    short_version = ".".join(v_parts[0:-1])

    return BuildJob(
        "julia",
        version,
        source_cmd="wget https://julialang-s3.julialang.org/bin/linux/x64/{short_version}/julia-{version}-linux-x86_64.tar.gz -P {env.source_path}".format(
            short_version=short_version, version=version
        ),
        configure_cmd="",
        build_cmd="",
        install_cmd=[
            "mkdir -p {env.install_path}",
            "tar -xf {env.source_path}/julia-{env.version}-linux-x86_64.tar.gz -C {env.install_path}",
        ],
    )


@build_task
def libefp(ctx, version="1.5.0"):
    """
    libefp -- a speedy semi-emperical library of nonsense
    """
    return BuildJob(
        "libefp",
        version,
        source_cmd="git clone --branch {env.version} https://github.com/ilyak/libefp.git {env.source_path}",
    )


@build_task
def mopac(ctx, version="2016"):
    """
    MOPAC -- A semi-emperical QM backend
    """
    zip_name = "MOPAC2016_for_Linux_64_bit.zip"

    return BuildJob(
        "mopac",
        version,
        source_cmd=f"wget http://openmopac.net/{zip_name} -P {env.source_path}",
        configure_cmd="",
        build_cmd="",
        install_cmd=[
            "mkdir -p {env.install_path}/bin",
            f"unzip {env.source_path}/{zip_name} -d {env.install_path}/bin/",
            "chmod u+x {env.install_path}/bin/MOPAC2016.exe",
        ],
    )


@build_task
def ninja(ctx, version="1.10.2"):
    """
    ninja -- speedy (and silent) build tool which eased QChem compilation
    """
    return BuildJob(
        "ninja",
        version,
        required_build_pkgs=["cmake", "gcc"],
        source_cmd="wget https://github.com/ninja-build/ninja/releases/download/v{env.version}/ninja-linux.zip -P {env.source_path}",
        configure_cmd="",
        build_cmd="",
        install_cmd=[
            "mkdir -p {env.install_path}/bin",
            "unzip {env.source_path}/ninja-linux.zip -d {env.install_path}/bin/",
        ],
    )


@build_task
def task_spooler(ctx, version="1.0.1"):
    """
    task_spooler -- task manger for CBEC computers
    """
    tar_name = "ts-{}.tar.gz".format(version)
    url = "https://vicerveza.homeunix.net/~viric/soft/ts/{}".format(tar_name)
    return BuildJob(
        "task_spooler",
        version,
        source_cmd=[
            "wget {} -P {env.source_path}".format(url),
            "tar -xf {env.source_path}/{} -C {env.source_path}".format(tar_name),
            "rm -rf {env.source_path}/{}".format(tar_name),
        ],
        configure_cmd="",
        build_cmd="make -C {env.source_path}/ts-{env.version} PREFIX={env.install_path} -j {env.nprocs}",
        install_cmd="make -C {env.source_path}/ts-{env.version} PREFIX={env.install_path} install",
    )
