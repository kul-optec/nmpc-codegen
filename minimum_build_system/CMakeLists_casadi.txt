set(files_casadi cost_function_derivative_combined.c cost_function.c)

if (EXISTS "${PROJECT_SOURCE_DIR}/casadi/integrator.c")
    set(files_casadi "${files_casadi}" integrator.c)
endif()

if(EXISTS "${PROJECT_SOURCE_DIR}/casadi/evaluate_constraints.c")
    set(files_casadi "${files_casadi}" evaluate_constraints.c)
endif()

MESSAGE(STATUS "Detected the following casadi files: ${files_casadi}")

add_library(CASADI_lib ${files_casadi})
set_property(TARGET CASADI_lib PROPERTY C_STANDARD 90)
set_property(TARGET CASADI_lib PROPERTY POSITION_INDEPENDENT_CODE ON) 