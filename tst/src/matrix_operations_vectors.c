/*
 * This file contains tests on the simple vector operations
 */

#include "../PANOC/matrix_operations.h"
#include "../globals/globals.h"
#include <stdio.h>

#define test_vector_size 4 /* use a small vector to do some simple tests */

int testVectorRealAdd(void);
int testVectorCopy(void);
int testVectoradd(void);
int testVectorsub(void);
int testVectorRealmul(void);

int main(){
    return testVectorRealAdd() \
    +testVectorCopy() \
    +testVectoradd() \
    +testVectorsub() \
    +testVectorRealmul();
}

/* 
 *vector:=vector+constant
 */
int testVectorRealAdd(void){
    real_t testVector[test_vector_size] = {1, 2, 3, 4};
    real_t testConstant = 1;
    vector_real_add(testVector,test_vector_size,testConstant,testVector);
        
    if(testVector[0]==2 && testVector[1]==3 && testVector[2]==4 && testVector[3]==5){ 
        return 0; /* sucess of test*/
    }else{
        printf("Adding [1 2 3 4] and 1 should result in [2 3 4 5] but resulted in [%f %f %f %f]",
            testVector[0],testVector[1],testVector[2],testVector[3]);
        return 1; /* test failed so return 1 */
    }
}

/*
 * test of vector copy
 */
 #define test_vector_size 4
int testVectorCopy(void){
    real_t testVector1[test_vector_size] = {1, 2, 3, 4};
    real_t testVector2[test_vector_size];

    vector_copy(testVector1,testVector2,test_vector_size);
    
    if(testVector2[0]==1 && testVector2[1]==2 && testVector2[2]==3 && testVector2[3]==4){ 
        return 0; /* sucess of test*/
    }else{
        printf("The copy should result in [1 2 3 4] but resulted in [%f %f %f %f]",
            testVector2[0],testVector2[1],testVector2[2],testVector2[3]);
        return 1; /* test failed so return 1 */
    }
}

/*
 * test of vector add
 */
int testVectoradd(void){
    real_t testVector1[test_vector_size] = {1, 2, 3, 4};
    real_t testVector2[test_vector_size] = {2, 3, 4, 5};

    vector_add(testVector1,testVector2,test_vector_size,testVector2);
    
    if(testVector2[0]==3 && testVector2[1]==5 && testVector2[2]==7 && testVector2[3]==9){ 
        return 0; /* sucess of test */
    }else{
        printf("Adding [1 2 3 4] with [2 3 4 5] should result in [3 5 7 9] but resulted in [%f %f %f %f]",
            testVector2[0],testVector2[1],testVector2[2],testVector2[3]);
        return 1; /* test failed so return 1 */
    }
}

/*
 * test of vector substraction
 */
int testVectorsub(void){
    real_t testVector1[test_vector_size] = {1, 2, 3, 4};
    real_t testVector2[test_vector_size] = {2, 3, 4, 5};

    vector_add(testVector1,testVector2,test_vector_size,testVector2);
    
    if(testVector2[0]==3 && testVector2[1]==5 && testVector2[2]==7 && testVector2[3]==9){ 
        return 0; /* sucess of test */
    }else{
        printf("the copy should result in [3 5 7 8] but resulted in [%f %f %f %f]",
            testVector2[0],testVector2[1],testVector2[2],testVector2[3]);
        return 1; /* test failed so return 1 */
    }
}

/*
 * test of vector real multiplication
 */
int testVectorRealmul(void){
    real_t testVector[test_vector_size] = {1, 2, 3, 4};
    real_t testReal =2;

    vector_real_mul(testVector,test_vector_size,testReal,testVector);
    
    if(testVector[0]==2 && testVector[1]==4 && testVector[2]==6 && testVector[3]==8){ 
        return 0; /* sucess of test */
    }else{
        printf("multiplying [1 2 3 4] with 2 should result in [2 4 6 8] but resulted in [%f %f %f %f]",
            testVector[0],testVector[1],testVector[2],testVector[3]);
        return 1; /* test failed so return 1 */
    }
}