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

/* add vector and real, put the result in vector */
void addVectorConstant(real_t* vector,size_t vector_size,real_t real){   
    for(;vector_size>0;vector_size--){
        *vector = *vector+real;
        vector++;
    }
}