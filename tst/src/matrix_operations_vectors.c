#include "../PANOC/matrix_operations.h"
#include "../globals/globals.h"
#include <stdio.h>

int testSimpleVectorConstantAdd(void);
int testVectorCopyMacro(void);

int main(){
    return testSimpleVectorConstantAdd()+testVectorCopyMacro();
}

/* 
 *vector:=vector+constant
 */
 #define size_testvector_vectorConstant 4
int testSimpleVectorConstantAdd(void){
    real_t testVector[size_testvector_vectorConstant] = {1, 2, 3, 4};
    real_t testConstant = 1;
    addVectorConstant(testVector,size_testvector_vectorConstant,testConstant);
    
    if(testVector[0]==2 && testVector[1]==3 && testVector[2]==4 && testVector[3]==5){ 
        return 0; /* sucess of test*/
    }else{
        printf("adding [1 2 3 4] and 1 should result in [2 3 4 5] but resulted in [%f %f %f %f]",
            testVector[0],testVector[1],testVector[2],testVector[3]);
        return 1; /* test failed so return 1 */
    }
}
/*
 * test of vector copy
 */
 #define size_testvector_copy 4
 int testVectorCopyMacro(void){
    real_t testVector1[size_testvector_copy] = {1, 2, 3, 4};
    real_t testVector2[size_testvector_copy];

    /* run the MACRO that needs testing*/
    VECTOR_COPY(testVector1,testVector2,size_testvector_copy)
    
    if(testVector2[0]==1 && testVector2[1]==2 && testVector2[2]==3 && testVector2[3]==4){ 
        return 0; /* sucess of test*/
    }else{
        printf("the copy should result in [1 2 3 4] but resulted in [%f %f %f %f]",
            testVector2[0],testVector2[1],testVector2[2],testVector2[3]);
        return 1; /* test failed so return 1 */
    }
}