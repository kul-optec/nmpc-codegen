### make sure the user is doing an our of source build:
if ( ${CMAKE_SOURCE_DIR} STREQUAL ${CMAKE_BINARY_DIR} )
    message( FATAL_ERROR "In-source builds are not allowed. use cmake -H. -Bbuild instead to build in the build folder" )
endif()
###

if (NOT EXISTS "${PROJECT_SOURCE_DIR}/casadi/cost_function_derivative_combined.c")
    message( FATAL_ERROR "Run generate_test_files.py first, with python3 and library casadi installed")
endif()

cmake_minimum_required (VERSION 2.6)
project (npmc C)
# set the compiler with its flags
# SET(CMAKE_C_COMPILER gcc)
SET(CMAKE_BUILD_TYPE Debug)
if(NOT MSVC)
    set(CMAKE_C_FLAGS_DEBUG "-g -O0 -Wall -Wextra -fprofile-arcs -ftest-coverage")
    set(LDFLAGS "-O0 -fprofile-arcs -ftest-coverage")
    SET(CMAKE_EXE_LINKER_FLAGS="-fprofile-arcs -ftest-coverage")
endif()

# subdirectories with libraries
include_directories ("${PROJECT_SOURCE_DIR}/PANOC")
add_subdirectory (PANOC) # read out the cmakelist file

include_directories ("${PROJECT_SOURCE_DIR}/casadi")
add_subdirectory (casadi)

# add the python interface, this target is excluded from all
if(WIN32)
    SET(TIMER_LIB "${PROJECT_SOURCE_DIR}/python_interface/timer_windows.c")
elseif(APPLE )
    SET(TIMER_LIB "${PROJECT_SOURCE_DIR}/python_interface/timer_empty.c" ) # TODO add timer class for mac's
else()
    SET(TIMER_LIB "${PROJECT_SOURCE_DIR}/python_interface/timer_linux.c" )
endif()

add_library(python_interface SHARED "${PROJECT_SOURCE_DIR}/python_interface/nmpc_python" "${TIMER_LIB}")
target_link_libraries (python_interface PANOC_lib)
target_link_libraries (python_interface CASADI_lib)
set_property(TARGET python_interface PROPERTY C_STANDARD 90)
set_property(TARGET python_interface PROPERTY POSITION_INDEPENDENT_CODE ON)
set_property(TARGET python_interface PROPERTY EXCLUDE_FROM_ALL TRUE)

# Test the functionality
enable_testing()
add_subdirectory(tst)

# Tests on the matrix/vector operations
add_test(NAME matrix_operations_norms COMMAND  tst/matrix_operations_norms)
add_test(NAME matrix_operations_vectors COMMAND  tst/matrix_operations_vectors)
add_test(NAME lbfgs_poly_test COMMAND  tst/lbfgs_poly_test)
#add_test(NAME lipschitz_estimator_test COMMAND  tst/lipschitz_estimator_test)
add_test(NAME prox_grad_descent_poly_test COMMAND  tst/prox_grad_descent_poly_test)
add_test(NAME panoc_poly_test COMMAND  tst/panoc_poly_test)
#add_test(NAME casadi_interface_test COMMAND  tst/casadi_interface_test)

add_custom_target(gcov
    COMMAND mkdir -p coverage
    COMMAND ${CMAKE_MAKE_PROGRAM} test
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    )

add_dependencies(gcov matrix_operations_norms)
add_dependencies(gcov matrix_operations_vectors)
add_dependencies(gcov lbfgs_poly_test)
#add_dependencies(gcov lipschitz_estimator_test)
add_dependencies(gcov prox_grad_descent_poly_test)
add_dependencies(gcov panoc_poly_test)
#add_dependencies(gcov casadi_interface_test)


add_custom_command(TARGET gcov
    COMMAND echo "=================== GCOV ===================="
    COMMAND gcov -b ${CMAKE_SOURCE_DIR}/panoc/*.c -o "${CMAKE_BINARY_DIR}/tst/CMakeFiles/matrix_operations_norms.dir/src/matrix_operations_norms.c.gcno"
    COMMAND gcov -b ${CMAKE_SOURCE_DIR}/panoc/*.c -o "${CMAKE_BINARY_DIR}/tst/CMakeFiles/matrix_operations_vectors.dir/src/matrix_operations_vectors.c.gcno"
    COMMAND gcov -b ${CMAKE_SOURCE_DIR}/panoc/*.c -o "${CMAKE_BINARY_DIR}/tst/CMakeFiles/lbfgs_poly_test.dir/src/lbfgs_poly_test.c.gcno"
    COMMAND gcov -b ${CMAKE_SOURCE_DIR}/panoc/*.c -o "${CMAKE_BINARY_DIR}/tst/CMakeFiles/prox_grad_descent_poly_test.dir/src/prox_grad_descent_poly_test.c.gcno"
    COMMAND gcov -b ${CMAKE_SOURCE_DIR}/panoc/*.c -o "${CMAKE_BINARY_DIR}/tst/CMakeFiles/panoc_poly_test.dir/src/panoc_poly_test.c.gcno"
    COMMAND echo "-- Coverage files have been output to ${CMAKE_BINARY_DIR}/coverage"
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/coverage 
    )