#include "../PANOC/matrix_operations.h"
#include "../globals/globals.h"
#include <stdio.h>

int test2norm(void);

int main(){
    return test2norm();
}

/* 
 * test the 2 norm: the 2 norm of [1 2 2 4] should be 5
 */
int test2norm(void){
    real_t testVector[4] = {1, 2, 2, 4};
    real_t testNorm = norm2_vector(testVector,4);
    if(testNorm==5){ 
        return 0;
    }else{
        printf("The 2 norm of [1; 2; 2; 4] should be 5 but is %f",testNorm);
        return 1; /* test failed so return 1 */
    }
}