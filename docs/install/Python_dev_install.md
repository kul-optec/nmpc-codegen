# How to compile and test me? (only for internal developers !)
This is only for those who want to check if the library works on there device. 
## Windows with Mingw/Mingw-W64 (!!! make sure python and the toolchain are either BOTH 32 or BOTH 64 bit)
- Generate the test functions by running the generate_test_files.py script with python3
- Run Cmake to generate the make files: cmake -H. -Bbuild -G "MinGW Makefiles"
- Run Make to compile everything: make
- Run make test to test everything: make test

## Unix-like operating systems
- Generate the test functions by running the generate_test_files.py script with python3
- Run Cmake to generate the make files: cmake -H. -Bbuild
- Run Make inside the ./build folder to compile everything: make
- Run make test to test everything: make test