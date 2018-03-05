### make sure the user is doing an our of source build:
if ( ${CMAKE_SOURCE_DIR} STREQUAL ${CMAKE_BINARY_DIR} )
    message( FATAL_ERROR "In-source builds are not allowed. use cmake -H. -Bbuild instead to build in the build folder" )
endif()
###

cmake_minimum_required (VERSION 2.6)
project (npmc C)
# set the compiler with its flags
SET(CMAKE_C_COMPILER gcc)
SET(CMAKE_BUILD_TYPE Debug)

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
add_test(NAME lipschitz_estimator_test COMMAND  tst/lipschitz_estimator_test)
add_test(NAME prox_grad_descent_poly_test COMMAND  tst/prox_grad_descent_poly_test)
add_test(NAME panoc_poly_test COMMAND  tst/panoc_poly_test)
add_test(NAME casadi_interface_test COMMAND  tst/casadi_interface_test)
