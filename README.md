# PANOC NMPC solver
## What is this?
This project is still under construction but the goal is to generate an MPC controller. The user will provide the dynamics of the system, a number of conditions and some MPC parameters in python. The program will then generate an NMPC controller in c89 code that can be used on embedded devices.

## What do I need?
- GNU toolchain with gcc
- python (both 2 and 3 work at this moment) with casadi installed on it
- Cmake (if you want to run the tests)

## How to compile and test me?
This is only for those who want to check if the library works on there device. 
### Windows with Mingw 
- Generate a test function python ./tst/python/generate_simple_func.py ./casadi/f.c
- Run Cmake to generate the make files: cmake . -G "MinGW Makefiles"
- Run Make to compile everything: make
- Run make test to test everything: make test

### Unix-like operating systems
- Generate a test function python ./tst/python/generate_simple_func.py ./casadi/f.c
- Run Cmake to generate the make files: cmake .
- Run Make to compile everything: make
- Run make test to test everything: make test