# lib with differnt f and g's in to use in tests
add_library(problem_set STATIC src/example_problems.c)
set_property(TARGET problem_set PROPERTY C_STANDARD 90)

# lib used when testing the lbfgs with polynomial, it replaces the prox grad descent with a mock
add_library(PANOC_test_lbfgs STATIC "${PROJECT_SOURCE_DIR}/PANOC/lbfgs.c" "${PROJECT_SOURCE_DIR}/PANOC/matrix_operations.c" src/mocks/lbfgs_test_proximal_gradient_descent.c)
set_property(TARGET PANOC_test_lbfgs PROPERTY C_STANDARD 90)

# from here on compile the different tests
add_executable(bin/matrix_operations_norms src/matrix_operations_norms.c)
target_link_libraries (bin/matrix_operations_norms PANOC_lib)
target_link_libraries(bin/matrix_operations_norms m) # link with the math lib, some toolchains need this

add_executable(bin/matrix_operations_vectors src/matrix_operations_vectors.c)
target_link_libraries (bin/matrix_operations_vectors PANOC_lib)
target_link_libraries(bin/matrix_operations_vectors m) # link with the math lib, some toolchains need this

add_executable(bin/panoc_interfaceCasadi_simpleTest src/panoc_interfaceCasadi_simpleTest.c)
target_link_libraries (bin/panoc_interfaceCasadi_simpleTest PANOC_lib)
target_link_libraries(bin/panoc_interfaceCasadi_simpleTest m) # link with the math lib, some toolchains need this

add_executable(bin/lbfgs_poly_test src/lbfgs_poly_test.c)
target_link_libraries (bin/lbfgs_poly_test PANOC_test_lbfgs)
target_link_libraries(bin/lbfgs_poly_test m) # link with the math lib, some toolchains need this
target_link_libraries(bin/lbfgs_poly_test problem_set)

add_executable(bin/lipschitz_estimator_test src/lipschitz_estimator_test.c)
target_link_libraries (bin/lipschitz_estimator_test PANOC_lib)
target_link_libraries(bin/lipschitz_estimator_test m) # link with the math lib, some toolchains need this

add_executable(bin/prox_grad_descent_poly_test src/prox_grad_descent_poly_test.c)
target_link_libraries (bin/prox_grad_descent_poly_test PANOC_fake)
target_link_libraries(bin/prox_grad_descent_poly_test m) # link with the math lib, some toolchains need this
target_link_libraries(bin/prox_grad_descent_poly_test problem_set)

add_executable(bin/panoc_poly_test src/panoc_poly_test.c)
target_link_libraries (bin/panoc_poly_test PANOC_fake)
target_link_libraries(bin/panoc_poly_test m) # link with the math lib, some toolchains need this
target_link_libraries(bin/panoc_poly_test problem_set)