#include"matrix_operations.h"
#include"math.h"

#include "stddef.h"

/*
 * calculate the 2 norm of a vector defined as
 * sqrt(x[0]^2 + x[1]^2 + ... x[n]^2)
 */
real_t norm2_vector(real_t* vector,size_t vector_size){
    real_t norm=0;
    for(int i=0;i<vector_size;i++){
        norm += pow(vector[i],2);
    }
    return sqrt(norm);
}

/* copy vector1 into vector2 */
void vector_copy(real_t* vector1,real_t* vector2,size_t size_vector){
    size_t i;
    for(i=0; i < size_vector; i++)vector2[i]=vector1[i];
}

/* add vector1 and vector2 save the result in result */
void vector_add(real_t* vector1,real_t* vector2,size_t size_vector,real_t* result){
    size_t i;
    for(i = 0; i < size_vector; i++)result[i]=vector1[i]+vector2[i];
}

/* add vector with real */
void vector_real_add(real_t* vector,size_t size_vector,real_t real,real_t* result){
    size_t i;
    for(i = 0; i < size_vector; i++)result[i]=vector[i]+real;
}

/* subtract vector2 from vector1 save the result in result */
void vector_sub(real_t* vector1,real_t* vector2,size_t size_vector,real_t* result){
    size_t i;
    for(i = 0; i < size_vector; i++)result[i]=vector1[i]-vector2[i];
}

/* multiply vector with real */
void vector_real_mul(real_t* vector,size_t size_vector,real_t real,real_t* result){
    size_t i;
    for(i = 0; i < size_vector; i++)result[i]=vector[i]*real;
}

/*  multiply each element of vector1 times -1 and save it in vector2 */
void vector_minus(real_t* vector1,real_t* vector2,size_t size_vector){
    while(size_vector>0){
        *vector2 = - *vector1;
        vector1++; vector2++;
        size_vector--;
    }
}

/* inner product between vector 1 and 2 */
real_t inner_product(real_t* vector1,real_t* vector2,size_t size_vector){
    size_t i;
    real_t result=0;
    for (i = 0; i < size_vector; i++)
    {
        result = result + vector1[i]*vector2[i];
    }
    return result;
}

/* add vector2 n times from vector1 */
void vector_add_ntimes(real_t* vector1,real_t* vector2,size_t size_vector,real_t n,real_t* result){
    size_t i;
    for(i = 0; i < size_vector; i++)result[i]=vector1[i]+n*vector2[i];
}