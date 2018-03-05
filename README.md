# PANOC NMPC solver
## What is this?
This project is still under construction but the goal is to generate an MPC controller. The user will provide the dynamics of the system, a number of conditions and some MPC parameters in python. The program will then generate an NMPC controller in c89 code that can be used on embedded devices.

Below here you can find a comparison between the Matlab implementation (ForBes zerofpr2) fmincon(interior point method of matlab) and nmpc-codegen. The time represents the time till convergence in milliseconds.(source code: ./demos/Matlab/compare_libs.m)

![alt text](trailer_example_time_log.png "Time till convergence simple simulation")

The first version of Python is ready to be used, a Matlab version is on its right now its experimental.(run ./demos/thesis/TwoCircTrailer.py to get an idea what this is about)

More information in the  [user manual](toturial.pdf) and the used [example script](toturial_nmpc_codegen.py). A short introduction to the underlying algorithm can be found [here](PANOC.pdf)

## What do I need?
- GNU toolchain with gcc
- python 3 with casadi and numpy installed on it
- Cmake

## How to compile and test me?
This is only for those who want to check if the library works on there device. 
### Windows with Mingw/Mingw-W64 (!!! make sure python and the toolchain are either BOTH 32 or BOTH 64 bit)
- Generate the test functions by running the generate_test_files.py script with python3
- Run Cmake to generate the make files: cmake -H. -Bbuild -G "MinGW Makefiles"
- Run Make to compile everything: make
- Run make test to test everything: make test

### Unix-like operating systems
- Generate the test functions by running the generate_test_files.py script with python3
- Run Cmake to generate the make files: cmake -H. -Bbuild
- Run Make inside the ./build folder to compile everything: make
- Run make test to test everything: make test

### Notes
- The tested compilers are gcc GNU compiler, Clang LLVM compiler and the Microsoft C Compiler.
- cmake -H. -Bbuild -DCMAKE_C_COMPILER=clang creates a build system with clang compiler

## common problems
1. When using the Matlab version the following error appears:
cmake: /usr/local/MATLAB/R2016a/bin/glnxa64/libcurl.so.4: no version information available (required by cmake)
cmake: /usr/local/MATLAB/R2016a/sys/os/glnxa64/libstdc++.so.6: version `GLIBCXX_3.4.18' not found (required by cmake)
cmake: /usr/local/MATLAB/R2016a/sys/os/glnxa64/libstdc++.so.6: version `CXXABI_1.3.9' not found (required by cmake)
cmake: /usr/local/MATLAB/R2016a/sys/os/glnxa64/libstdc++.so.6: version `GLIBCXX_3.4.20' not found (required by cmake)
cmake: /usr/local/MATLAB/R2016a/sys/os/glnxa64/libstdc++.so.6: version `GLIBCXX_3.4.21' not found (required by cmake)
cmake: /usr/local/MATLAB/R2016a/sys/os/glnxa64/libstdc++.so.6: version `GLIBCXX_3.4.21' not found (required by /usr/lib/x86_64-linux-gnu/libjsoncpp.so.1)
cmake: /usr/local/MATLAB/R2016a/sys/os/glnxa64/libstdc++.so.6: version `CXXABI_1.3.8' not found (required by /usr/lib/x86_64-linux-gnu/libicuuc.so.57)

This is due to Matlab using some old version from gcc. 

solution: start matlab as following: "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6 matlab" 
