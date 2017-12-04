# PANOC NMPC solver
## What is this?
This project is still under construction but the goal is to generate an MPC controller. The user will provide the dynamics of the system, a number of conditions and some MPC parameters in python. The program will then generate an NMPC controller in c89 code that can be used on embedded devices.

## What do I need?
- GNU toolchain with gcc
- python 3 with casadi and numpy installed on it
- Cmake

## How to compile and test me?
This is only for those who want to check if the library works on there device. 
### Windows with Mingw (!!! make sure python and the toolchain are either BOTH 32 or BOTH 64 bit)
- Generate the test functions by running the generate_test_files.py script with python3
- Run Cmake to generate the make files: cmake . -G "MinGW Makefiles"
- Run Make to compile everything: make
- Run make test to test everything: make all test

### Unix-like operating systems
- Generate the test functions by running the generate_test_files.py script with python3
- Run Cmake to generate the make files: cmake .
- Run Make to compile everything: make
- Run make test to test everything: make all test