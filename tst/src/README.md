# Test on C code
This folder contains software tests on the static C code. The globals file and cost function are mocks and are generated trough python scripts. See more about this on the main page.

## Tests on the linear algebra
The matrix_operations.c/.h files contain linear algebra operations. As NMPC-codegen is aimed at embedded devices it cannot use the commonly used library's for these operations. 
### Tests on norms (matrix_operations_norms.c)
### Tests on vector operations (matrix_operations_vectors.c)
### Tests on matrix operations (no tests of this type yet)