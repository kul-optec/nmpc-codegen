#include"matrix_operations.h"
#include"math.h"

#include "stddef.h"

/*
 * calculate the 2 norm of a vector defined as
 * sqrt(x[0]^2 + x[1]^2 + ... x[n]^2)
 */
real_t vector_norm2(const real_t* vector,const size_t vector_size){
    real_t norm=0;
    size_t i;
    for(i=0;i<vector_size;i++){
        norm += pow(vector[i],2);
    }
    return sqrt(norm);
}

/* calculate the 1 norm */
real_t vector_norm1(const real_t* vector,const size_t vector_size){
    real_t norm=0;

    size_t i=0;
    for ( i = 0; i < vector_size ; i++)
    {
        norm += ABS(vector[i]);
    }
    return norm;
}

real_t vector_norm_inf(const real_t* vector,const size_t vector_size){
    real_t norm=0;

    size_t i=0;
    for ( i = 0; i < vector_size ; i++)
    {
        if(norm<ABS(vector[i]))
            norm = ABS(vector[i]);
    }
    return norm;
}


/* copy vector1 into vector2 */
void vector_copy(const real_t* vector1,real_t* vector2,const size_t size_vector){
    size_t i;
    for(i=0; i < size_vector; i++)vector2[i]=vector1[i];
}

/* add vector1 and vector2 save the result in result */
void vector_add(const real_t* vector1,const real_t* vector2,const size_t size_vector,real_t* result){
    size_t i;
    for(i = 0; i < size_vector; i++)result[i]=vector1[i]+vector2[i];
}

/* add vector with real */
void vector_real_add(const real_t* vector,const size_t size_vector,const real_t real,real_t* result){
    size_t i;
    for(i = 0; i < size_vector; i++)result[i]=vector[i]+real;
}

/** subtract vector2 from vector1 save the result in result */
void vector_sub(const real_t* vector1,const real_t* vector2,const size_t size_vector,real_t* result){
    size_t i;
    for(i = 0; i < size_vector; i++)result[i]=vector1[i]-vector2[i];
}

/* multiply vector with real */
void vector_real_mul(const real_t* vector,const size_t size_vector,const real_t real,real_t* result){
    size_t i;
    for(i = 0; i < size_vector; i++)result[i]=vector[i]*real;
}

/*  multiply each element of vector1 times -1 and save it in vector2 */
void vector_minus(const real_t* vector1,real_t* vector2,const size_t size_vector){
    size_t i;
    for(i = 0; i < size_vector; i++)vector2[i]=-vector1[i];
}

/* inner product between vector 1 and 2 */
real_t inner_product(const real_t* vector1,const real_t* vector2,const size_t size_vector){
    size_t i;
    real_t result=0;
    for (i = 0; i < size_vector; i++)
    {
        result = result + vector1[i]*vector2[i];
    }
    return result;
}

/* add vector2 n times to vector1 */
void vector_add_ntimes(const real_t* vector1,const real_t* vector2,const size_t size_vector,const real_t n,real_t* result){
    size_t i;
    for(i = 0; i < size_vector; i++)result[i]=vector1[i]+n*vector2[i];
}

/* add vector2 a_vector2 times to vector1 and add vector3 a_vector3 times to vector1*/
void vector_add_2_vectors_a_times(const real_t* vector1,const real_t* vector2,const real_t* vector3,const size_t size_vector,
    const real_t a_vector2,const real_t a_vector3,real_t* result){
    size_t i;
    for(i = 0; i < size_vector; i++)result[i]=vector1[i]+a_vector2*vector2[i]+a_vector3*vector3[i];
}