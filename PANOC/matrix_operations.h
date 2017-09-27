#ifndef MATRIX_OPERATIONS_H
#define MATRIX_OPERATIONS_H

#include "../globals/globals.h"
#include "stddef.h"
#include "math.h"
 
/* 2 norm with preprocessor */


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

/*
 * calculate the 2 norm of a vector defined as
 * sqrt(x[0]^2 + x[1]^2 + ... x[n]^2)
 */
real_t vector_norm2(real_t* vector,size_t vector_size);

/*  multiply each element of vector1 times -1 and save it in vector2 */
void vector_minus(real_t* vector1,real_t* vector2,size_t size_vector);

/* inner product between vector 1 and 2 */
real_t inner_product(real_t* vector1,real_t* vector2,size_t size_vector);

/* add vector2 n times to vector1 */
void vector_add_ntimes(real_t* vector1,real_t* vector2,size_t size_vector,real_t n,real_t* result);

#endif