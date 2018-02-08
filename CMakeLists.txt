cmake_minimum_required (VERSION 2.6)
project (npmc C)

# set the compiler with its flags
SET(CMAKE_C_COMPILER gcc)
SET(CMAKE_BUILD_TYPE Debug)

add_definitions(-Wall)
add_definitions(-Wextra)

# subdirectories with libraries
include_directories ("${PROJECT_SOURCE_DIR}/PANOC")
add_subdirectory (PANOC) # read out the cmakelist file

include_directories ("${PROJECT_SOURCE_DIR}/casadi")
add_subdirectory (casadi)

# add the python interface, this target is excluded from all
if(WIN32)
    SET(TIMER_LIB "${PROJECT_SOURCE_DIR}/python_interface/timer_windows.c")
elseif(UNIX)
    SET(TIMER_LIB "${PROJECT_SOURCE_DIR}/python_interface/timer_linux.c")
endif()

add_library(python_interface SHARED "${PROJECT_SOURCE_DIR}/python_interface/nmpc_python" "${TIMER_LIB}")
target_link_libraries (python_interface PANOC_lib)
set_property(TARGET python_interface PROPERTY C_STANDARD 90)
set_property(TARGET python_interface PROPERTY POSITION_INDEPENDENT_CODE ON)
set_property(TARGET python_interface PROPERTY EXCLUDE_FROM_ALL TRUE)

# Test the functionality
enable_testing()
add_subdirectory(tst)

# Tests on the matrix/vector operations
add_test(NAME matrix_operations_norms COMMAND  tst/bin/matrix_operations_norms)
add_test(NAME matrix_operations_vectors COMMAND  tst/bin/matrix_operations_vectors)
add_test(NAME lbfgs_poly_test COMMAND  tst/bin/lbfgs_poly_test)
add_test(NAME lipschitz_estimator_test COMMAND  tst/bin/lipschitz_estimator_test)
add_test(NAME prox_grad_descent_poly_test COMMAND  tst/bin/prox_grad_descent_poly_test)
add_test(NAME panoc_poly_test COMMAND  tst/bin/panoc_poly_test)
add_test(NAME casadi_interface_test COMMAND  tst/bin/casadi_interface_test)