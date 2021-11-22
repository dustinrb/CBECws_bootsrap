from copy import copy
from invoke import Task, task

from tasks.build.BuildRunner import BashRunner, PrintRunner
from tasks.build.BuildJob import BuildJob
from tasks.build.LMod import is_loaded


INSTALL_KWARGS = [
    "source",
    "configure",
    "build",
    "install",
]

class BuildTask(Task):

    def argspec(self, body):
        """
            Adds additional build args to control how things are built
        """
        arg_names, spec_dict = super().argspec(body)
        
        self._org_arg_names = copy(arg_names)

        for a in INSTALL_KWARGS:
            arg_names.append(a)
            spec_dict[a] = False
        return arg_names, spec_dict


    def __call__(self, *args, **kwargs):
        # Get a copy of the compile options
        build_args = {k: v for k, v in kwargs.items() if k in INSTALL_KWARGS}
        for a in INSTALL_KWARGS:
            del kwargs[a]

        job = super().__call__(*args, **kwargs)
        assert type(job) == BuildJob
        ctx = args[0]

        if not any(build_args.values()):
            job.runner = PrintRunner()
            job.install()
            job.run()
        else:
            job.runner = BashRunner()
            if build_args["install"]:
                job.install()
            elif build_args["configure"]:
                job.configure()
            elif build_args["build"]:
                job.build()
            elif build_args["source"]:
                job.source()
            job.run()


def build_task(*args, **kwargs):
    kwargs.setdefault("klass", BuildTask)
    return task(*args, **kwargs) 


@build_task
def armadillo(ctx, version="10.2.x"):
    """
    C++ matrix library in headers
    """
    return BuildJob(
        "armadillo",
        version,
        source_cmd="git clone --branch $pkg_version https://gitlab.com/conradsnicta/armadillo-code.git $pkg_src"
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
        source_cmd="git clone --branch llvmorg-$pkg_version https://github.com/llvm/llvm-project.git $pkg_src",
        configure_cmd=[
            "CC=gcc CXX=g++ cmake -G\"$pkg_cmake_build_tool\" "
            "-B $pkg_build_path "
            "-DCMAKE_INSTALL_PREFIX=$pkg_install_path "
            "-DCMAKE_CXX_LINK_FLAGS=-Wl,-rpath,/opt/modules/gcc/7.3/lib64 -L/opt/modules/gcc/7.3/lib64 "
            "-DLLVM_ENABLE_PROJECTS='clang;clang-tools-extra;libcxx;libcxxabi;openmp;parallel-libs;' "
            "-DLLVM_TARGETS_TO_BUILD=\"X86\" "
            "-DCMAKE_BUILD_TYPE=Release "
            "-DLLVM_BUILD_EXAMPLES=OFF " 
            "-DLLVM_INCLUDE_EXAMPLES=OFF "
            "-DLLVM_BUILD_TESTS=OFF "
            "-DLLVM_INCLUDE_TESTS=OFF "
            "-DLLVM_INCLUDE_BENCHMARKS=OFF "
            "-DLLVM_TEMPORARILY_ALLOW_OLD_TOOLCHAIN=YES "
            "$pkg_src/llvm "
        ],
        build_cmd="cmake --build . -j $nprocs",
        install_cmd="cmake --install $pkg_build_path"
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
        source_cmd="git clone --branch $pkg_version https://gitlab.com/libeigen/eigen.git $pkg_src"
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
        source_cmd="git clone --branch $pkg_version https://github.com/fish-shell/fish-shell.git $pkg_src",
        configure_cmd="CC=gcc CXX=g++ cmake -B $pkg_build_path -G\"$pkg_cmake_build_tool\" -DCMAKE_INSTALL_PREFIX=$pkg_install_path $pkg_src",
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
        source_cmd="git clone git@gitlab.com:forthehorde/fragment.git $pkg_src",
        configure_cmd="CC=mpicc CXX=mpic++ LD=mpic++ cmake -B $pkg_build_path -DCMAKE_INSTALL_PREFIX=$pkg_install_path -DCMAKE_EXPORT_COMPILE_COMMANDS=yes $pkg_src",
        build_cmd=[
            "cmake --build $pkg_build_path -- -j $nprocs",
            "sed  -i 's/-qopenmp/-fopenmp/g' $pkg_build_path/compile_commands.json",
            "ln -s $pkg_build_path/compile_commands.json $pkg_src/"
        ]
    )


# @build_task
# def gcc_compatibility(ctx, version="7.3"):
#     """
#     gcc_compatibility -- Makes newer GCC libs available while having Intel compilers loaded
#     """
#     return BuildJob(
#         "gcc_compatibility",
#         version,
#         source_cmd="mkdir -p $pkg_src",
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
    url = "https://github.com/evaleev/libint/releases/download/v{version}/{tf}".format(version=version, tf=tar_file)

    return BuildJob(
        "libint",
        version,
        source_cmd=[
            "wget {} -P $pkg_src".format(url),
            "tar -xf $pkg_src/{} -C $pkg_src".format(tar_file),
            "rm -rf $pkg_src/{}".format(tar_file),
            "mv $pkg_src/{}/* ./".format(base_folder)
        ]
    )


@build_task
def qcaux(ctx, version="trunk"):
    """
    qcaux -- basis set definitions for QChem
    """
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
            "QCBUILD=$pkg_rel_src_to_build "
            "./configure intel mkl openmp relwdeb nointracule nomgc noccman2 "
            "{btf} --prefix=$pkg_install_path".format(btf=build_tool_flag)
        ],
        build_cmd=[
            "cmake -B $pkg_build_path -DCMAKE_EXPORT_COMPILE_COMMANDS=YES $pkg_src",
            "cmake --build $pkg_build_path --target qcprog.exe -- -j $nprocs"
        ],
        install_cmd=[
            "cmake --install $pkg_build_path",
            "[[ ! -L $pkg_install_path/bin/mpi ]] && ln -s $pkg_src/bin/mpi $pkg_install_path/bin/mpi"
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


@build_task
def git(ctx, version="2.29.2"):
    """
    git -- newer version of git needed for VSCode
    """
    return BuildJob(
        "git",
        version,
        source_cmd="git clone --branch v$pkg_version https://github.com/git/git.git $pkg_src",
        configure_cmd="",
        build_cmd="make -C $pkg_src prefix=$pkg_install_path -j $nprocs",
        install_cmd="make -C $pkg_src prefix=$pkg_install_path install"
    )


@build_task
def julia(ctx, version="1.5.3"):
    """
    julia -- Julia programming language
    """
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


@build_task
def libefp(ctx, version="1.5.0"):
    """
    libefp -- a speedy semi-emperical library of nonsense
    """
    return BuildJob(
        "libefp",
        version,
        source_cmd="git clone --branch $pkg_version https://github.com/ilyak/libefp.git $pkg_src"
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
        source_cmd=f"wget http://openmopac.net/{zip_name} -P $pkg_src",
        configure_cmd="",
        build_cmd="",
        install_cmd=[
            "mkdir -p $pkg_install_path/bin",
            f"unzip $pkg_src/{zip_name} -d $pkg_install_path/bin/",
            "chmod u+x $pkg_install_path/bin/MOPAC2016.exe"
        ]
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
        source_cmd="wget https://github.com/ninja-build/ninja/releases/download/v$pkg_version/ninja-linux.zip -P $pkg_src",
        configure_cmd="",
        build_cmd="",
        install_cmd=[
            "mkdir -p $pkg_install_path/bin",
            "unzip $pkg_src/ninja-linux.zip -d $pkg_install_path/bin/"
        ]
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
            "wget {} -P $pkg_src".format(url),
            "tar -xf $pkg_src/{} -C $pkg_src".format(tar_name),
            "rm -rf $pkg_src/{}".format(tar_name)
        ],
        configure_cmd="",
        build_cmd="make -C $pkg_src/ts-$pkg_version PREFIX=$pkg_install_path -j $nprocs",
        install_cmd="make -C $pkg_src/ts-$pkg_version PREFIX=$pkg_install_path install"
    )