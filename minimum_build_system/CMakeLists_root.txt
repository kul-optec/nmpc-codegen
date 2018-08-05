cmake_minimum_required (VERSION 2.6)
project (npmc_minimum C)

# set the compiler with its flags
SET(CMAKE_C_COMPILER gcc)

# if not specified assume release.
# specify that you want debug with: cmake . -DCMAKE_BUILD_TYPE=Debug
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

if(NOT MSVC)
  set(CMAKE_C_FLAGS_DEBUG "-g -Wall -Wextra")
  set(CMAKE_C_FLAGS_RELEASE "-O3")
endif()

# subdirectory with lib
include_directories ("${PROJECT_SOURCE_DIR}/PANOC")
add_subdirectory (PANOC) # read out the cmakelist file

include_directories ("${PROJECT_SOURCE_DIR}/casadi")
add_subdirectory (casadi)

if(WIN32)
    SET(TIMER_LIB "${PROJECT_SOURCE_DIR}/python_interface/timer_windows.c")
elseif(APPLE)
    SET(TIMER_LIB "${PROJECT_SOURCE_DIR}/python_interface/timer_mac.c" )
elseif(UNIX)
    SET(TIMER_LIB "${PROJECT_SOURCE_DIR}/python_interface/timer_linux.c")
endif()

add_library(python_interface SHARED "${PROJECT_SOURCE_DIR}/python_interface/nmpc_python" "${TIMER_LIB}")
target_link_libraries (python_interface PANOC_lib CASADI_lib)
set_property(TARGET python_interface PROPERTY C_STANDARD 90)
set_property(TARGET python_interface PROPERTY POSITION_INDEPENDENT_CODE ON)

SET(MAIN_FILE_PATH "${PROJECT_SOURCE_DIR}/main.c" )

if (EXISTS "${MAIN_FILE_PATH}")
    MESSAGE( STATUS "main.c detected use 'make main_exe' to compile it" )
    add_executable(main_exe "${MAIN_FILE_PATH}")
    target_link_libraries (main_exe PANOC_lib CASADI_lib)
    target_link_libraries(main_exe m) # link with the math lib, some toolchains need this
else()
    MESSAGE( STATUS "No main.c detected in project root folder" )
endif()