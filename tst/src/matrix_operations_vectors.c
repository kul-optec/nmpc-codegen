/*
 * This file contains tests on the simple vector operations
 */

#include "../PANOC/matrix_operations.h"
#include "../globals/globals.h"
#include <stdio.h>

#define test_vector_size 4 /* use a small vector to do some simple tests */

int test_vectorRealAdd(void);
int test_vectorCopy(void);
int test_vectoradd(void);
int test_vectorsub(void);
int test_vectorRealmul(void);
int test_vector_minus(void);
int test_vector_add_ntimes(void);
int test_vector_add_2_vectors_a_times(void);

int main(){
    return test_vectorRealAdd() \
    +test_vectorCopy() \
    +test_vectoradd() \
    +test_vectorsub() \
    +test_vectorRealmul() \
    +test_vector_minus() \
    +test_vector_add_ntimes()\
    +test_vector_add_2_vectors_a_times();
}

/* 
 *vector:=vector+constant
 */
int test_vectorRealAdd(void){
    real_t test_vector[test_vector_size] = {1, 2, 3, 4};
    real_t testConstant = 1;
    vector_real_add(test_vector,test_vector_size,testConstant,test_vector);
        
    if(test_vector[0]==2 && test_vector[1]==3 && test_vector[2]==4 && test_vector[3]==5){ 
        return 0; /* sucess of test*/
    }else{
        printf("Adding [1 2 3 4] and 1 should result in [2 3 4 5] but resulted in [%f %f %f %f]",
            test_vector[0],test_vector[1],test_vector[2],test_vector[3]);
        return 1; /* test failed so return 1 */
    }
}

/*
 * test of vector copy
 */
 #define test_vector_size 4
int test_vectorCopy(void){
    real_t test_vector1[test_vector_size] = {1, 2, 3, 4};
    real_t test_vector2[test_vector_size];

    vector_copy(test_vector1,test_vector2,test_vector_size);
    
    if(test_vector2[0]==1 && test_vector2[1]==2 && test_vector2[2]==3 && test_vector2[3]==4){ 
        return 0; /* sucess of test*/
    }else{
        printf("The copy should result in [1 2 3 4] but resulted in [%f %f %f %f]",
            test_vector2[0],test_vector2[1],test_vector2[2],test_vector2[3]);
        return 1; /* test failed so return 1 */
    }
}

/*
 * test of vector add
 */
int test_vectoradd(void){
    real_t test_vector1[test_vector_size] = {1, 2, 3, 4};
    real_t test_vector2[test_vector_size] = {2, 3, 4, 5};

    vector_add(test_vector1,test_vector2,test_vector_size,test_vector2);
    
    if(test_vector2[0]==3 && test_vector2[1]==5 && test_vector2[2]==7 && test_vector2[3]==9){ 
        return 0; /* sucess of test */
    }else{
        printf("Adding [1 2 3 4] with [2 3 4 5] should result in [3 5 7 9] but resulted in [%f %f %f %f]",
            test_vector2[0],test_vector2[1],test_vector2[2],test_vector2[3]);
        return 1; /* test failed so return 1 */
    }
}

/*
 * test of vector substraction
 */
int test_vectorsub(void){
    real_t test_vector1[test_vector_size] = {1, 2, 3, 4};
    real_t test_vector2[test_vector_size] = {2, 3, 4, 5};

    vector_add(test_vector1,test_vector2,test_vector_size,test_vector2);
    
    if(test_vector2[0]==3 && test_vector2[1]==5 && test_vector2[2]==7 && test_vector2[3]==9){ 
        return 0; /* sucess of test */
    }else{
        printf("the copy should result in [3 5 7 8] but resulted in [%f %f %f %f]",
            test_vector2[0],test_vector2[1],test_vector2[2],test_vector2[3]);
        return 1; /* test failed so return 1 */
    }
}

/*
 * test of vector real multiplication
 */
int test_vectorRealmul(void){
    real_t test_vector[test_vector_size] = {1, 2, 3, 4};
    real_t testReal =2;

    vector_real_mul(test_vector,test_vector_size,testReal,test_vector);
    
    if(test_vector[0]==2 && test_vector[1]==4 && test_vector[2]==6 && test_vector[3]==8){ 
        return 0; /* sucess of test */
    }else{
        printf("multiplying [1 2 3 4] with 2 should result in [2 4 6 8] but resulted in [%f %f %f %f]",
            test_vector[0],test_vector[1],test_vector[2],test_vector[3]);
        return 1; /* test failed so return 1 */
    }
}

int test_vector_minus(void){
    real_t test_vector[test_vector_size] = {1, 2, 3, 4};
    vector_minus(test_vector,test_vector,test_vector_size);
    if(test_vector[0]==-1 && test_vector[1]==-2 && test_vector[2]==-3 && test_vector[3]==-4){ 
        return SUCCESS; /* sucess of test */
    }else{
        printf("multiplying [1 2 3 4] with -1 should result in [-1 -2 -3 -4] but resulted in [%f %f %f %f]",
            test_vector[0],test_vector[1],test_vector[2],test_vector[3]);
        return FAILURE; /* test failed so return 1 */
    }
    
}

int test_vector_add_ntimes(void){
    real_t test_vector1[test_vector_size] = {1, 2, 3, 4};
    real_t test_vector2[test_vector_size] = {1, 1, 2, 2};
    real_t test_scalar=2;

    vector_add_ntimes(test_vector1,test_vector2,test_vector_size,test_scalar);

    if(test_vector1[0]==3 && test_vector1[1]==4 && test_vector1[2]==7 && test_vector1[3]==8){ 
        return SUCCESS; /* sucess of test */
    }else{
        printf("adding [1 2 3 4] with 2 times [1 1 2 2] and should result in [3 4 7 8] but resulted in [%f %f %f %f]",
            test_vector1[0],test_vector1[1],test_vector1[2],test_vector1[3]);
        return FAILURE; /* test failed so return 1 */
    }
}

int test_vector_add_2_vectors_a_times(void){
    real_t test_vector1[test_vector_size] = {1, 2, 3, 4};
    real_t test_vector2[test_vector_size] = {1, 1, 2, 2};
    real_t a2=-1;
    real_t test_vector3[test_vector_size] = {2, 2, 1, 1};
    real_t a3=1;

    vector_add_2_vectors_a_times(test_vector1,test_vector2,test_vector3,test_vector_size,a2,a3,test_vector1);

    if(test_vector1[0]==2 && test_vector1[1]==3 && test_vector1[2]==2 && test_vector1[3]==3){ 
        return SUCCESS; /* sucess of test */
    }else{
        printf("Test should result in [2 3 2 3] but resulted in [%f %f %f %f]",
            test_vector1[0],test_vector1[1],test_vector1[2],test_vector1[3]);
        return FAILURE; /* test failed so return 1 */
    }
}