from BuildRunner import BuildRunner, PrintRunner, BashRunner
from BuildJob import BuildJob
from LMod import is_loaded


def clangd(version="11.0.0"):
    return BuildJob(
        "clangd",
        version,
        required_build_pkgs=["cmake", "gcc"],
        required_pkgs=["gcc_compatibility"],
        source_cmd="git clone --branch llvmorg-$pkg_version https://github.com/llvm/llvm-project.git $pkg_src",
        configure_cmd=[
            "CC=gcc CXX=g++ cmake -G\"$pkg_cmake_build_tool\" "
            "-B $pkg_build_path "
            "-DCMAKE_INSTALL_PREFIX=$pkg_install_path "
            "-DLLVM_ENABLE_PROJECTS='clang;clang-tools-extra' "
            "-DLLVM_TARGETS_TO_BUILD=\"X86\" "
            "-DCMAKE_BUILD_TYPE=Release "
            "-DLLVM_BUILD_EXAMPLES=OFF " 
            "-DLLVM_INCLUDE_EXAMPLES=OFF "
            "-DLLVM_BUILD_TESTS=OFF "
            "-DLLVM_INCLUDE_TESTS=OFF "
            "-DLLVM_INCLUDE_BENCHMARKS=OFF "
            "$pkg_src/llvm"
        ],
    )

def eigen(version="3.3.9"):
    return BuildJob(
        "eigen",
        version,
        required_build_pkgs=["cmake"],
        source_cmd="git clone --branch $pkg_version https://gitlab.com/libeigen/eigen.git $pkg_src",
        configure_cmd="cmake -B $pkg_build_path -G\"$pkg_cmake_build_tool\" -DCMAKE_INSTALL_PREFIX=$pkg_install_path $pkg_src",
    )


def fish(version="3.1.2"):
    return BuildJob(
        "fish",
        version,
        required_build_pkgs=["cmake", "intel"],
        source_cmd="git clone --branch $pkg_version https://github.com/fish-shell/fish-shell.git $pkg_src",
        configure_cmd="CC=gcc CXX=g++ cmake -B $pkg_build_path -G\"$pkg_cmake_build_tool\" -DCMAKE_INSTALL_PREFIX=$pkg_install_path $pkg_src",
    )


def fragment(version="master"):
    return BuildJob(
        "fragment",
        version,
        required_build_pkgs=["cmake"],
        required_pkgs=["intel", "mpi"],
        source_cmd="git clone git@gitlab.com:forthehorde/fragment.git $pkg_src",
        configure_cmd="CC=mpicc CXX=mpic++ LD=mpic++ cmake -B $pkg_build_path -DCMAKE_INSTALL_PREFIX=$pkg_install_path -DCMAKE_EXPORT_COMPILE_COMMANDS=yes $pkg_src",
        build_cmd=[
            "cmake --build $pkg_build_path -- -j $nprocs",
            "sed  -i 's/-qopenmp/-fopenmp/g' $pkg_build_path/compile_commands.json",
            "ln -s $pkg_build_path/compile_commands.json $pkg_src/"
        ]
    )


def gcc_compatibility(version="7.3"):
    return BuildJob(
        "gcc_compatibility",
        version,
        source_cmd="mkdir -p $pkg_src",
        configure_cmd="",
        build_cmd="",
        install_cmd=""
    )

def qcaux(version="trunk"):
    return BuildJob(
        "qcaux",
        version,
        source_cmd=[
            "svn co https://jubilee.q-chem.com/svnroot/qcaux/trunk $pkg_install_path",
            "wget https://downloads.q-chem.com/qcinstall/drivers/drivers.linux.tar.gz -P $pkg_install_path/"
        ],
        configure_cmd="",
        build_cmd="",
        install_cmd="tar xzf $pkg_install_path/drivers.linux.tar.gz -C $pkg_install_path"
    ) 


def qchem(version="trunk"):
    SVN_ROOT = "https://jubilee.q-chem.com/svnroot/qchem"

    # Choose the correct branching information 
    version = version.strip()
    if version == "trunk":
        source_url = "{}/{}".format(SVN_ROOT, version)         
    else:
        source_url = "{}/branches/{}".format(SVN_ROOT, version)

    # Provide an option to use ninja (NINJA!)
    if is_loaded("ninja"):
        build_tool_flag = "ninja "
    else:
        build_tool_flag = ""

    return BuildJob(
        "qchem",
        version,
        source_cmd="svn co {} $pkg_src".format(source_url),
        configure_cmd=[
            "QCBUILD=$pkg_rel_src_to_build ./configure intel mkl openmp relwdeb nointracule nomgc nodmrg noccman2 {btf} --prefix=$pkg_install_path".format(btf=build_tool_flag)
        ],
        build_cmd=[
            "cmake -B $pkg_build_path -DCMAKE_EXPORT_COMPILE_COMMANDS=YES $pkg_src",
            "cmake --build $pkg_build_path -- -j $nprocs",
            "clangify_compile_commands.py $pkg_build_path/compile_commands.json > $pkg_src/compile_commands.json",
        ],
        install_cmd=[
            "cmake --install $pkg_build_path",
            "[[ ! -L $pkg_install_path/bin/mpi ]] && ln -s $pkg_src/bin/mpi $pkg_install_path/bin/mpi"
        ],
        required_pkgs=["intel", "mkl"],
        required_build_pkgs=["cmake"],
    )


def qchem_dailyref(version="trunk"):
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
        source_cmd="svn co {} $pkg_src".format(source_url),
        configure_cmd="",
        build_cmd="",
        install_cmd=[
            "mkdir -p $ENV_PATH/qchem_dailyref",
            "[[ ! -L $pkg_install_path ]] && ln -s $pkg_src $pkg_install_path",
            "svn up $pkg_src"
        ],
        required_pkgs=[],
        required_build_pkgs=[],
    )


def git(version="2.29.2"):
    return BuildJob(
        "git",
        version,
        required_build_pkgs=["cmake"],
        source_cmd="git clone --branch v$pkg_version https://github.com/git/git.git $pkg_src",
        configure_cmd="",
        build_cmd="make -C $pkg_src prefix=$pkg_install_path -j $nprocs",
        install_cmd="make -C $pkg_src prefix=$pkg_install_path install"
    )


def julia(version="1.5.3"):
    v_parts = version.split('.')
    short_version = ".".join(v_parts[0:-1])

    return BuildJob(
        "julia",
        version,
        source_cmd="wget https://julialang-s3.julialang.org/bin/linux/x64/{short_version}/julia-{version}-linux-x86_64.tar.gz -P $pkg_src".format(
            short_version=short_version,
            version=version
        ),
        configure_cmd="",
        build_cmd="",
        install_cmd=[
            "mkdir -p $pkg_install_path",
            "tar -xf $pkg_src/julia-$pkg_version-linux-x86_64.tar.gz -C $pkg_install_path"
        ]
    )


def ninja(version="1.10.2"):
    return BuildJob(
        "ninja",
        version,
        required_build_pkgs=["cmake", "gcc"],
        source_cmd="wget https://github.com/ninja-build/ninja/releases/download/v$pkg_version/ninja-linux.zip -P $pkg_src",
        configure_cmd="",
        build_cmd="",
        install_cmd=[
            "mkdir -p $pkg_install_path/bin",
            "unzip $pkg_src/ninja-linux.zip -d $pkg_install_path/bin/"
        ]
    ) 
