#include"../../../globals/globals.h"
#include"../../../PANOC/buffer.h"
#include <stddef.h>
#include <stdlib.h>
#include "../example_problems.h"

/* functions not used by lbfgs test */
int proximal_gradient_descent_init(size_t dimension, \
    real_t (*g_)(const real_t* input), \
    void (*proxg_)(const real_t* input, real_t* output),\
    real_t (*f_)(const real_t* input),\
    void (*df_)(const real_t* input, real_t* output)){return SUCCESS;}
int proximal_gradient_descent_cleanup(void){return SUCCESS;}
const real_t* proximal_gradient_descent_get_direction(const real_t* current_location){return 0;}
real_t proximal_gradient_descent_forward_backward_envelop(const real_t* current_location){return 0;}
real_t proximal_gradient_descent_get_gamma(void){return 0;}

/*
 * function used with lbgfs, replace this with a polynomial, initialize the polynomial first !
 */
int proximal_gradient_descent_get_residual(const real_t* input,real_t* output){
    df_poly(input,output);
    return SUCCESS;
}
int proximal_gradient_descent_get_current_residual(real_t* residual){
    proximal_gradient_descent_get_residual(buffer_get_current_location(),residual);
    return SUCCESS;
}