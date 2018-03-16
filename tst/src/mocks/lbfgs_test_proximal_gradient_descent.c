#include"../../../globals/globals.h"
#include"../../../PANOC/buffer.h"
#include <stddef.h>
#include <stdlib.h>
#include "../example_problems.h"

/* functions not used by lbfgs test */
/*
int proximal_gradient_descent_cleanup(void){return SUCCESS;}
const real_t* proximal_gradient_descent_get_direction(const real_t* current_location){return 0;}
real_t proximal_gradient_descent_forward_backward_envelop(const real_t* current_location){return 0;}

*/

static unsigned char rosenbrock = FALSE;
int enable_rosenbrock(void){
    rosenbrock=TRUE;
    return SUCCESS;
}
int disable_rosenbrock(void){
    rosenbrock=FALSE;
    return SUCCESS;
}

real_t proximal_gradient_descent_get_gamma(void){return 1;}

real_t* buffer;
int lbfgs_prox_grad_descent_test_init(int dimension){
    buffer = malloc(dimension*sizeof(real_t));
    return SUCCESS;
}
int lbfgs_prox_grad_descent_test_cleanup(void){
    free(buffer);
    return SUCCESS;
}
const real_t* proximal_gradient_descent_get_buffered_direction(void){
    if(rosenbrock==TRUE)
        df_rosenbrock(buffer_get_current_location(),buffer);
    else
        df_poly(buffer_get_current_location(),buffer);
    return buffer;
}

/*
 * function used with lbgfs, replace this with a polynomial or rosenbrock function, initialize the polynomial first !
 */
int proximal_gradient_descent_get_residual(const real_t* input,real_t* output){
    if(rosenbrock==TRUE)
        df_rosenbrock(input,output);
    else
        df_poly(input,output);
    return SUCCESS;
}
int proximal_gradient_descent_get_current_residual(real_t* residual){
    proximal_gradient_descent_get_residual(buffer_get_current_location(),residual);
    return SUCCESS;
}

int proximal_gradient_descent_get_new_residual(const real_t* input,real_t* output){
    if(rosenbrock==TRUE)
        df_rosenbrock(input,output);
    else
        df_poly(input,output);
    return SUCCESS;
}
/*
 * compute residual using direction used by fordward backward envelop
 */
int proximal_gradient_descent_get_new_residual_buffered(real_t* residual){
    return SUCCESS;
}