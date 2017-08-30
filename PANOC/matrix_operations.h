 #ifndef MATRIX_OPERATIONS_H
 #define MATRIX_OPERATIONS_H

 #include "../globals/globals.h"
 #include "stddef.h"
 
 /* 2 norm with preprocessor */
 /*
 #define NORM2_VECTOR(vector,vector_size,norm)(\
     norm=0;\
     sqrt(for(int i=0,i<vector_size,i++){buffer+=vector[i]}\
 )
 */

real_t norm2_vector(real_t* vector,size_t vector_size);

#endif