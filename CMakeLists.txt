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

# example of a test
# 
# add_test(NAME testAddTest COMMAND  tests/bin/testAdd)