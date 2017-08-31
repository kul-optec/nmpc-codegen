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
#define VECTOR_COPY(vector1,vector2,size_vector) for(size_t i = 0; i < size_vector; i++)vector2[i]=vector1[i];

/* add vector1 and vector2 save the result in result */
#define VECTOR_ADD(vector1,vector2,size_vector,result) for(size_t i = 0; i < size_vector; i++)result[i]=vector1[i]+vector2[i];

/* add vector with real */
#define VECTOR_REAL_ADD(vector,size_vector,real,result)for(size_t i = 0; i < size_vector; i++)result[i]=vector[i]+real;

/* subtract vector2 from vector1 save the result in result */
#define VECTOR_SUB(vector1,vector2,size_vector,result) for(size_t i = 0; i < size_vector; i++)result[i]=vector1[i]-vector2[i];

/* multiply vector with real */
#define VECTOR_REAL_MUL(vector,size_vector,real,result)for(size_t i = 0; i < size_vector; i++)result[i]=vector[i]*real;

real_t norm2_vector(real_t* vector,size_t vector_size);
void addVectorConstant(real_t* vector1,size_t vector1_size,real_t real);

#endif