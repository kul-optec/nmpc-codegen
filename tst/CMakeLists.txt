# add_custom_command(
#     OUTPUT ${PROJECT_SOURCE_DIR}/casadi/f.c
#     WORKING_DIR ${CMAKE_SOURCE_DIR}
#     COMMAND python ./python/generate_simple_func.py ../casadi/f.c
#     DEPENDS ${PROJECT_SOURCE_DIR}/PANOC/interfaceCasadi.c ${PROJECT_SOURCE_DIR}/tst/src/panoc_interfaceCasadi_simpleTest.c
#     VERBATIM
# )

add_executable(bin/matrix_operations_norms src/matrix_operations_norms.c)
target_link_libraries (bin/matrix_operations_norms PANOC_lib)
target_link_libraries(bin/matrix_operations_norms m) # link with the math lib, some toolchains need this

add_executable(bin/matrix_operations_vectors src/matrix_operations_vectors.c)
target_link_libraries (bin/matrix_operations_vectors PANOC_lib)
target_link_libraries(bin/matrix_operations_vectors m) # link with the math lib, some toolchains need this

add_executable(bin/panoc_interfaceCasadi_simpleTest src/panoc_interfaceCasadi_simpleTest.c)
target_link_libraries (bin/panoc_interfaceCasadi_simpleTest PANOC_lib)
target_link_libraries(bin/panoc_interfaceCasadi_simpleTest m) # link with the math lib, some toolchains need this

add_library(problem_set STATIC src/example_problems.c)
set_property(TARGET problem_set PROPERTY C_STANDARD 90)

add_executable(bin/lbfgs_poly_test src/lbfgs_poly_test.c)
target_link_libraries (bin/lbfgs_poly_test PANOC_lib)
target_link_libraries(bin/lbfgs_poly_test m) # link with the math lib, some toolchains need this

add_executable(bin/lipschitz_estimator_test src/lipschitz_estimator_test.c)
target_link_libraries (bin/lipschitz_estimator_test PANOC_lib)
target_link_libraries(bin/lipschitz_estimator_test m) # link with the math lib, some toolchains need this

add_executable(bin/prox_grad_descent_poly_test src/prox_grad_descent_poly_test.c)
target_link_libraries (bin/prox_grad_descent_poly_test PANOC_lib)
target_link_libraries(bin/prox_grad_descent_poly_test m) # link with the math lib, some toolchains need this
target_link_libraries(bin/prox_grad_descent_poly_test problem_set)

add_executable(bin/panoc_poly_test src/panoc_poly_test.c)
target_link_libraries (bin/panoc_poly_test PANOC_lib)
target_link_libraries(bin/panoc_poly_test m) # link with the math lib, some toolchains need this
target_link_libraries(bin/panoc_poly_test problem_set)