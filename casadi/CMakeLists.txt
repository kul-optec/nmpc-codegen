if (EXISTS integrator.c)
    set(files_casadi cost_function_derivative_combined.c cost_function.c integrator.c)
else()
    set(files_casadi cost_function_derivative_combined.c cost_function.c)
endif()

add_library(CASADI_lib ${files_casadi})
set_property(TARGET CASADI_lib PROPERTY C_STANDARD 90)
set_property(TARGET CASADI_lib PROPERTY POSITION_INDEPENDENT_CODE ON) 