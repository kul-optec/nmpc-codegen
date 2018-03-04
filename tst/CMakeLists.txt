# lib with differnt f and g's in to use in tests
add_library(problem_set STATIC src/example_problems.c)
set_property(TARGET problem_set PROPERTY C_STANDARD 90)

# lib used when testing the lbfgs with polynomial, it replaces the prox grad descent with a mock
add_library(PANOC_test_lbfgs STATIC "${PROJECT_SOURCE_DIR}/PANOC/lbfgs.c" "${PROJECT_SOURCE_DIR}/PANOC/matrix_operations.c" src/mocks/lbfgs_test_proximal_gradient_descent.c src/mocks/lbfgs_test_buffer.c )
set_property(TARGET PANOC_test_lbfgs PROPERTY C_STANDARD 90)

# from here on compile the different tests
add_executable(matrix_operations_norms src/matrix_operations_norms.c)
target_link_libraries(matrix_operations_norms PANOC_lib)
if(NOT MSVC)
target_link_libraries(matrix_operations_norms m) # link with the math lib, some toolchains need this
endif()

add_executable(matrix_operations_vectors src/matrix_operations_vectors.c)
target_link_libraries (matrix_operations_vectors PANOC_lib)
if(NOT MSVC)
target_link_libraries(matrix_operations_vectors m) # link with the math lib, some toolchains need this
endif()

add_executable(lbfgs_poly_test src/lbfgs_poly_test.c)
target_link_libraries (lbfgs_poly_test PANOC_test_lbfgs)
if(NOT MSVC)
target_link_libraries(lbfgs_poly_test m) # link with the math lib, some toolchains need this
endif()
target_link_libraries(lbfgs_poly_test problem_set)

add_executable(lipschitz_estimator_test src/lipschitz_estimator_test.c)
target_link_libraries (lipschitz_estimator_test PANOC_fake)
if(NOT MSVC)
target_link_libraries(lipschitz_estimator_test m) # link with the math lib, some toolchains need this
endif()
target_link_libraries(lipschitz_estimator_test problem_set)

add_executable(prox_grad_descent_poly_test src/prox_grad_descent_poly_test.c)
target_link_libraries (prox_grad_descent_poly_test PANOC_fake)
if(NOT MSVC)
target_link_libraries(prox_grad_descent_poly_test m) # link with the math lib, some toolchains need this
endif()
target_link_libraries(prox_grad_descent_poly_test problem_set)

add_executable(panoc_poly_test src/panoc_poly_test.c)
target_link_libraries (panoc_poly_test PANOC_fake)
if(NOT MSVC)
target_link_libraries(panoc_poly_test m) # link with the math lib, some toolchains need this
endif()
target_link_libraries(panoc_poly_test problem_set)

add_executable(casadi_interface_test src/casadi_interface_test.c)
target_link_libraries (casadi_interface_test PANOC_lib)
if(NOT MSVC)
target_link_libraries(casadi_interface_test m) # link with the math lib, some toolchains need this
endif()
target_link_libraries(casadi_interface_test CASADI_lib) 
