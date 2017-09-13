#include<stdio.h>
#include<math.h>
#include"../../PANOC/lbfgs.h"
#include"../../globals/globals.h"

int checkIfSolutionIsReached(void);
/*
 * TEST lbfgs
 * polynomial f(x1,x2,x3) = x1^4+x2^4+ x3^4+x1^3+x2^3+ x3^3
 * f(x) =0 if x=[0 0 0 0]
 */
int main(){
    return checkIfSolutionIsReached(); 
}

int checkIfSolutionIsReached(void){
    const real_t* theoretical_solution={0,0,0,0};

    lbfgs_init();
    
    lbfgs_cleanup();

    return FAILURE; /* test is not ready yet return failure */
}