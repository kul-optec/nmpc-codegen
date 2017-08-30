cmake_minimum_required (VERSION 2.6)
project (npmc)

# set the compiler with its flags
SET(CMAKE_C_COMPILER gcc)
SET(CMAKE_BUILD_TYPE Debug)
SET(GCC_COVERAGE_COMPILE_FLAGS "-Wall -std=c99")

# subdirectories with libraries
include_directories ("${PROJECT_SOURCE_DIR}/PANOC")
add_subdirectory (PANOC) # read out the cmakelist file

# Test the functionality
enable_testing()
add_subdirectory(tst)

# Tests on the matrix/vector operations
add_test(NAME matrix_operations_2norm COMMAND  tst/bin/matrix_operations_2norm)