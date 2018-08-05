#ifndef MATRIX_OPERATIONS_H
#define MATRIX_OPERATIONS_H

#include "../globals/globals.h"
#include "stddef.h"
#include "math.h"
 
/* squared with preprocessor */
#define sq(x) ((x)*(x))


/* copy vector1 into vector2 */
void vector_copy(const real_t* vector1,real_t* vector2,const int size_vector);

/* add vector1 and vector2 save the result in result */
void vector_add(const real_t* vector1,const real_t* vector2,const int size_vector,real_t* result);

/* add vector with real */
void vector_real_add(const real_t* vector,const int size_vector,const real_t real,real_t* result);

/* subtract vector2 from vector1 save the result in result */
void vector_sub(const real_t* vector1,const real_t* vector2,const int size_vector,real_t* result);

/* multiply vector with real */
void vector_real_mul(const real_t* vector,const int size_vector,const real_t real,real_t* result);

/*
 * calculate the 2 norm of a vector defined as
 * sqrt(x[0]^2 + x[1]^2 + ... x[n]^2)
 */
real_t vector_norm2(const real_t* vector,const int vector_size);

real_t vector_norm1(const real_t* vector,const int vector_size);

real_t vector_norm_inf(const real_t* vector,const int vector_size);

real_t vector_norm_max(const real_t* vector,const int vector_size);

real_t vector_norm_min(const real_t* vector,const int vector_size);

real_t vector_norm_inf_signed(const real_t* vector,const int vector_size);

int vector_norm_inf_element_index(const real_t* vector,const int vector_size);

/*  multiply each element of vector1 times -1 and save it in vector2 */
void vector_minus(const real_t* vector1,real_t* vector2,const int size_vector);

/* inner product between vector 1 and 2 */
real_t inner_product(const real_t* vector1,const real_t* vector2,const int size_vector);

/* add vector2 n times to vector1 */
void vector_add_ntimes(real_t* vector1,const real_t* vector2,const int size_vector,const real_t n);

/* add vector2 a_vector2 times to vector1 and add vector3 a_vector3 times to vector1*/
void vector_add_2_vectors_a_times(const real_t* vector1,const real_t* vector2,const real_t* vector3,const int size_vector,
    const real_t a_vector2,const real_t a_vector3,real_t* result);

#endif