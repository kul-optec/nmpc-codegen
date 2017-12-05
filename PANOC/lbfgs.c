#include"lbfgs.h"
#include"buffer.h"
#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>
#include "matrix_operations.h"
#include "proximal_gradient_descent.h"

/* 
 * The following two matrices are safed between iterations 
 * s = [s0 s1 ... sn] with s1 the most recent s and sn the oldest s 
 * In short this means that the vector s0 can be found in s[0]
 *
 * y has the same format as s
 */
static real_t** s; /* s_k = x_{k+1} - x_{k} */
static real_t** y; /* y_k = gradient(x_{k+1}) - gradient(x_{k}) */

/* 2 arrays that not need to be saved between iterations */
static real_t* alpha;
static real_t* rho;


static size_t iteration_index=0; /* the iteration index, this is increased at the end of the iteration */
static size_t buffer_size; /* buffersize initialized in init method */
static size_t dimension;
static real_t* direction;

void shift_s_and_y(const size_t buffer_limit); /* internal function used to shift the s and y buffers */

static real_t* y_data; /* data field used to allocate 2D array y, if only one malloc is used we get cast errors */
static real_t* s_data; /* data field used to allocate 2D array s, if only one malloc is used we get cast errors */

/*
 * Initialize the lbfgs library
 * This function should allways be called before doing anything with the lbfgs algorithm.
 */
int lbfgs_init(const size_t buffer_size_,const size_t dimension_){
    
    dimension=dimension_;
    buffer_size=buffer_size_;
    iteration_index=0;

    /* 
     * Allocate memory.
     */
    s_data = malloc(sizeof(real_t)*dimension*buffer_size);
    if(s_data==NULL) goto fail_1;

    s = malloc(sizeof(real_t)*buffer_size);
    if(s==NULL) goto fail_2;

    y_data = malloc(sizeof(real_t)*dimension*buffer_size);
    if(y_data==NULL) goto fail_3;

    y = malloc(sizeof(real_t)*buffer_size);
    if(y==NULL) goto fail_4;

    alpha = malloc(sizeof(real_t)*buffer_size);
    if(alpha==NULL) goto fail_5;

    rho = malloc(sizeof(real_t)*buffer_size);
    if(rho==NULL) goto fail_6;

    direction =malloc(sizeof(real_t)*dimension);
    if(rho==NULL) goto fail_7;
    /*
     * if all the allocations took place, setup the 2D arrays
     */
    size_t i;
    for (i = 0; i < buffer_size; i++)
    {
        s[i] = s_data + i*dimension;
        y[i] = y_data + i*dimension;
    }

    return SUCCESS;

    /*
     * Something went wrong free up the necessary memory and return failure
     */
    fail_7:
        free(rho);
    fail_6:
        free(alpha);
    fail_5:
        free(y);
    fail_4: 
        free(y_data);
    fail_3: 
        free(s);
    fail_2: 
        free(s_data);
    fail_1:
        return FAILURE;
}

/*
 * cleanup the lbfgs library
 * This function cleans up the memory used by the lbfgs algorithm, 
 * use this when you don't need the lib anymore
 */
int lbfgs_cleanup(void){
        free(s_data);
        free(s);
        free(y_data);
        free(y);
        free(alpha);
        free(rho);
        iteration_index=0;
        return SUCCESS;
}
int lbfgs_reset_iteration_counters(void){
    iteration_index=0;
    return SUCCESS;
}

/*
 * returns the direction calculated with lbfgs
 */ 
const real_t* lbfgs_get_direction(void){
    const real_t* current_location = buffer_get_current_location();
    real_t q[dimension];proximal_gradient_descent_get_residual(current_location,q);

    /* 
     * If the residual is about zero then this is a fixed point, 
     * set the direct on zero and return.
     */
    if(vector_norm2(q,dimension)<MACHINE_ACCURACY){
        size_t i;
        for ( i = 0; i < dimension; i++)
        {
            direction[i]=0;
        }
        return direction;
    }

    /* is this the first time you call get_direction? */
    if(iteration_index==0){
        /* 
         * use gradient descent for first iteration 
         */
        vector_minus(q,direction,dimension); /* set the direction */
    }else{
        size_t buffer_limit; /* how much of the buffer should i use in this iteration? */
        if(iteration_index<buffer_size){
            buffer_limit=iteration_index;
        }else{
            buffer_limit=buffer_size;
        }

        /*
        * First loop lbfgs
        */
        int i;/*"i" should be able to go negative, as this is used in second loop */
        for (i = 0; i < buffer_limit; i++)
        {
            rho[i] = 1/inner_product(y[i],s[i],dimension);
            alpha[i]= rho[i]*inner_product(s[i],q,dimension);
            vector_add_ntimes(q,y[i],dimension,-alpha[i],q);
        }

        
        real_t z[dimension];
        vector_real_mul(y[buffer_limit-1], \
            dimension, \
            inner_product(s[buffer_limit-1],q,dimension)*(1/inner_product(y[buffer_limit-1],y[buffer_limit-1], \
            dimension)), \
            z);
        /*
        * Second loop lbfgs
        */
        real_t beta;
        for (i = buffer_limit - 1; i >= 0; i--)
        {
            beta=rho[i]*inner_product(y[i],z,dimension);
            vector_add_ntimes(z,s[i],dimension,(alpha[i]-beta),z); 
        }
        vector_minus(z,direction,dimension); /* z contains upward direction, multiply with -1 to get downward direction */

        shift_s_and_y(buffer_limit); /* prepare s and y for new values */
    }

    real_t new_location[dimension]; 
    vector_add(current_location,direction,dimension,new_location); /* get the new location */

    vector_sub(new_location,current_location,dimension,s[0]); /* set s */
    
    real_t gradient_current_location[dimension];proximal_gradient_descent_get_current_residual(gradient_current_location);/* find df(x) */
    real_t gradient_new_location[dimension];proximal_gradient_descent_get_residual(new_location,gradient_new_location); /* find df(new_x) */

    vector_sub(gradient_new_location,gradient_current_location,dimension,y[0]); /* set y=df(new_x) - df(x) */

    iteration_index++;
    return direction;
}

 /* internal function used to shift the s and y buffers */
void shift_s_and_y(const size_t buffer_limit){
        real_t* buffer_s =s[buffer_size-1];
        real_t* buffer_y =y[buffer_size-1];
        size_t i;
        for (i = buffer_size-1; i >0 ; i--)
        {
            s[i] = s[i-1];
            y[i] = y[i-1];
        }
        s[0]=buffer_s;
        y[0]=buffer_y;
}