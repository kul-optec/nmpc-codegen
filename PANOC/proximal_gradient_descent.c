#include "proximal_gradient_descent.h"
#include "casadi_interface.h"
#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>
#include "matrix_operations.h"
#include "lipschitz.h"
#include"buffer.h"

/* functions only used internally */
int proximal_gradient_descent_check_linesearch();
int proximal_gradient_descent_forward_backward_step(const real_t* location);

/* values set by the init function */
static size_t dimension;

/* variables safed between direction calls */
static size_t iteration_index=0; /* is 0 at first and 1 after first time you call get direction */
static real_t linesearch_gamma=0; /* linesearch parameter */

/* variables used by each iteration */
static real_t* new_location;
static real_t* direction;

int proximal_gradient_descent_init(){
    dimension=casadi_interface_get_dimension();

    new_location = malloc(sizeof(real_t*)*dimension);
    if(new_location==NULL)goto fail_1;

    direction = malloc(sizeof(real_t*)*dimension);
    if(direction==NULL)goto fail_2;

    return SUCCESS;

    /*
     * something went wrong when allocating memory, free up what was already taken
     */
    fail_2:
        free(new_location);
    fail_1:
        return FAILURE;
}
int proximal_gradient_descent_cleanup(void){
    free(new_location);
    free(direction);
    return SUCCESS;
}
/*
 * Find the proximal gradient descent with linesearch
 */
const real_t* proximal_gradient_descent_get_direction(){
   /* 
    * If this is the first time you call me, find the initial gamma value
    * by estimating the lipschitz value of df
    */
    const real_t* current_location = buffer_get_current_location();
    if(iteration_index==0){
        real_t lipschitz_value = get_lipschitz(current_location);

        linesearch_gamma = (1-PROXIMAL_GRAD_DESC_SAFETY_VALUE)/lipschitz_value;
        iteration_index++; /* index only needs to increment if it is 0 */
    }
    proximal_gradient_descent_forward_backward_step(current_location);
    while(proximal_gradient_descent_check_linesearch()==FAILURE){
        linesearch_gamma=linesearch_gamma/2;
        proximal_gradient_descent_forward_backward_step(current_location);
    }
    return direction;
}
/* 
 * This function performs an forward backward step. x=prox(x-gamma*df(x))
 */
int proximal_gradient_descent_forward_backward_step(const real_t* location){
    real_t buffer[dimension];
    casadi_interface_df(location,buffer); /* buffer = current gradient (at location) */
    vector_add_ntimes(location,buffer,dimension,-1*linesearch_gamma,buffer); /* buffer = location - gamma * buffer */
    casadi_interface_proxg(buffer,new_location); /* new_location = proxg(buffer) */
    vector_sub(new_location,location,dimension,direction); /* find the direction */
    return SUCCESS;
}

/*
 * returns the residual, R(x) = 1/gamma[ x- proxg(x-df(x)*gamma)]
 */
int proximal_gradient_descent_get_residual(const real_t* location,real_t* residual){
    proximal_gradient_descent_forward_backward_step(location);
    vector_sub(location,new_location,dimension,residual);
    vector_real_mul(residual,dimension,1/linesearch_gamma,residual);
    return SUCCESS;
}

/*
 * returns the residual using the previous forward backward step, R(x) = 1/gamma[ x- proxg(x-df(x)*gamma)]
 */
int proximal_gradient_descent_get_current_residual(real_t* residual){
    const real_t* current_location = buffer_get_current_location();
    vector_sub(current_location,new_location,dimension,residual);
    vector_real_mul(residual,dimension,1/linesearch_gamma,residual);
    return SUCCESS;
}

/*
 * check if the linesearch condition is satisfied
 */
int proximal_gradient_descent_check_linesearch(){
    const real_t* df_current_location=buffer_get_current_df();
    const real_t inner_product_df_direction = inner_product(df_current_location,direction,dimension);

    const real_t f_current_location=buffer_get_current_f();
    const real_t f_new_location=casadi_interface_f(new_location);

    const real_t norm_direction = pow(vector_norm2(direction,dimension),2);

    if(f_new_location>f_current_location - inner_product_df_direction + ( (1-PROXIMAL_GRAD_DESC_SAFETY_VALUE)/2 )*(norm_direction/linesearch_gamma) )
        return FAILURE;
    else
        return SUCCESS;
}

/*
 * calculate the forward backward envelop using the internal gamma
 * Matlab cache.FBE = cache.fx + cache.gz - cache.gradfx(:)'*cache.FPR(:) + (0.5/gam)*(cache.normFPR^2);
 */
real_t proximal_gradient_descent_forward_backward_envelop(const real_t* current_location){
    proximal_gradient_descent_forward_backward_step(current_location); /* this will fill the new_direction variable */

    const real_t f_current_location=casadi_interface_f(current_location);
    real_t df_current_location[dimension];casadi_interface_df(current_location,df_current_location);
    const real_t g_new_location=casadi_interface_g(new_location);

    const real_t norm_direction = pow(vector_norm2(direction,dimension),2);

    const real_t forward_backward_envelop = f_current_location + g_new_location \
     - inner_product(df_current_location,direction,dimension) \
     + (1/(linesearch_gamma*2))*norm_direction;

     return forward_backward_envelop;
}

real_t proximal_gradient_descent_get_gamma(void){
    return linesearch_gamma;
}