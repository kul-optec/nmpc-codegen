# PANOC NMPC solver
## What is this?
Nmpc-codegen generates MPC controllers. The user provides the dynamics of the system, a number of conditions and some MPC parameters in python. Nmpc-codegen will then generate the NMPC controller in c89 code that can be used on embedded devices. Check out the [website](https://kul-forbes.github.io/nmpc-codegen/) for more information.

If you want to use this library for research feel free to contact willem.melis at student.kuleuven.be .

More information in the  [user manual](toturial.pdf) and the used [example script](toturial_nmpc_codegen.py). A short introduction to the underlying algorithm can be found [here](PANOC.pdf)

## How to install?
- [Matlab](https://kul-forbes.github.io/nmpc-codegen/install/Python_install.html)
- [Python](https://kul-forbes.github.io/nmpc-codegen/install/Matlab_install.html)

## How to compile and test me?
This is only for those who want to check if the library works on there device. 
### Windows with Mingw/Mingw-W64 (!!! make sure python and the toolchain are either BOTH 32 or BOTH 64 bit)
- Generate the test functions by running the generate_test_files.py script with python3
- Run Cmake to generate the make files: cmake -H. -Bbuild -G "MinGW Makefiles"
- Run Make to compile everything: make
- Run make test to test everything: make test

![alt text](trailer_example_time_log.png "Time till convergence simple simulation")

## Notes
- The library is tested with casadi version 3.2, using other versions will lead to problems
- The tested compilers on the raw controller code are gcc GNU compiler, Clang LLVM compiler, Intel C compiler and the Microsoft C Compiler.
- cmake -H. -Bbuild -DCMAKE_C_COMPILER=clang creates a build system with clang compiler and Cmake