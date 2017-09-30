#include "../PANOC/matrix_operations.h"
#include "../globals/globals.h"
#include <stdio.h>

int test2norm(void); 
int test_inner_product(void);
int test2norm_floating_point(void);
int testnorm_floating_point(void);

int main(){
    return test2norm()+\
    test_inner_product()+\
    test2norm_floating_point()+\
    testnorm_floating_point();
}

/* 
 * test the 2 norm: the 2 norm of [1 2 2 4] should be 5
 */
int test2norm(void){
    real_t testVector[4] = {1, 2, 2, 4};
    real_t testNorm = vector_norm2(testVector,4);
    if(testNorm==5){ 
        return SUCCESS;
    }else{
        printf("The 2 norm of [1; 2; 2; 4] should be 5 but is %f",testNorm);
        return FAILURE; /* test failed so return 1 */
    }
}

int test2norm_floating_point(void){
    real_t testVector[4] = {0.1, 0.2, 0.2, 0.4};
    real_t testNorm = vector_norm2(testVector,4);
    if(testNorm==0.5){ 
        return SUCCESS;
    }else{
        printf("The 2 norm of [0.1; 0.2; 0.2; 0.4] should be 0.5 but is %f",testNorm);
        return FAILURE; /* test failed so return 1 */
    }
}

int testnorm_floating_point(void){
    real_t testVector[4] = {-0.1, -0.2, 0.2, 0.4};
    real_t testNorm = vector_norm1(testVector,4);
    if(testNorm==0.9){ 
        return SUCCESS;
    }else{
        printf("The 1 norm of [-0.1; -0.2; 0.2; 0.4] should be 0.9 but is %f",testNorm);
        return FAILURE; /* test failed so return 1 */
    }
}


int test_inner_product(void){
    real_t test_vector1[4] = {1, 2, 3, 4};
    real_t test_vector2[4] = {1, 2, 3, 4};

    real_t inner_product_test =inner_product(test_vector1,test_vector2,4);
    if(inner_product_test==30){ 
        return SUCCESS;
    }else{
        printf("The innerproduct of [1; 2; 3; 4] with [1; 2; 3; 4]  should be 30 but is %f",inner_product_test);
        return FAILURE; /* test failed so return 1 */
    }
}