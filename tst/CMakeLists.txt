# add_custom_command(
#     OUTPUT ${PROJECT_SOURCE_DIR}/casadi/f.c
#     WORKING_DIR ${CMAKE_SOURCE_DIR}
#     COMMAND python ./python/generate_simple_func.py ../casadi/f.c
#     DEPENDS ${PROJECT_SOURCE_DIR}/PANOC/interfaceCasadi.c ${PROJECT_SOURCE_DIR}/tst/src/panoc_interfaceCasadi_simpleTest.c
#     VERBATIM
# )

add_executable(bin/matrix_operations_norms src/matrix_operations_norms.c)
target_link_libraries (bin/matrix_operations_norms PANOC_lib)

add_executable(bin/matrix_operations_vectors src/matrix_operations_vectors.c)
target_link_libraries (bin/matrix_operations_vectors PANOC_lib)

add_executable(bin/panoc_interfaceCasadi_simpleTest src/panoc_interfaceCasadi_simpleTest.c)
target_link_libraries (bin/panoc_interfaceCasadi_simpleTest PANOC_lib)