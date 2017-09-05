#ifndef MATRIX_OPERATIONS_H
#define MATRIX_OPERATIONS_H

#include "../globals/globals.h"
#include "stddef.h"
#include "math.h"
 
/* 2 norm with preprocessor */

#define VECTOR_2NORM(vector,vector_size,norm)\
    norm=0;\
    for(int i=0;i<vector_size;i++)norm+=pow(vector[i],2);\
    norm = sqrt(norm);

/* copy vector1 into vector2 */
void vector_copy(real_t* vector1,real_t* vector2,size_t size_vector);

/* add vector1 and vector2 save the result in result */
void vector_add(real_t* vector1,real_t* vector2,size_t size_vector,real_t* result);

/* add vector with real */
void vector_real_add(real_t* vector,size_t size_vector,real_t real,real_t* result);

/* subtract vector2 from vector1 save the result in result */
void vector_sub(real_t* vector1,real_t* vector2,size_t size_vector,real_t* result);

/* multiply vector with real */
void vector_real_mul(real_t* vector,size_t size_vector,real_t real,real_t* result);

real_t norm2_vector(real_t* vector,size_t vector_size);
void addVectorConstant(real_t* vector1,size_t vector1_size,real_t real);

#endif