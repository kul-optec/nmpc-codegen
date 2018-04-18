#include"lbfgs.h"
#include"buffer.h"
#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>
#include "matrix_operations.h"
#include "proximal_gradient_descent.h"
#include "math.h"

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


static unsigned int active_buffer_size=0; /* the used buffer size , this is increased at the end of an hessian update */
static unsigned int buffer_size; /* buffersize initialized in init method */
static real_t* direction;

static void shift_s_and_y(void); /* internal function used to shift the s and y buffers */
static int check_if_valid_update(const real_t* gradient_current_location); /* internal function used to check if the new s and y should be saved */

static real_t* y_data; /* data field used to allocate 2D array y, if only one malloc is used we get cast errors */
static real_t* s_data; /* data field used to allocate 2D array s, if only one malloc is used we get cast errors */
static real_t hessian_estimate=0;

static int lbfgs_reset_direction(void); /* internal function */

/*
 * Initialize the lbfgs library
 * This function should allways be called before doing anything with the lbfgs algorithm.
 */
int lbfgs_init(const unsigned int buffer_size_){
    buffer_size=buffer_size_;
    active_buffer_size=0;

    /* 
     * Allocate memory.
     */
    s_data = malloc(sizeof(real_t)*DIMENSION_PANOC*(buffer_size+1));
    if(s_data==NULL) goto fail_1;

    s = malloc(sizeof(real_t*)*(buffer_size+1));
    if(s==NULL) goto fail_2;

    y_data = malloc(sizeof(real_t)*DIMENSION_PANOC*(buffer_size+1));
    if(y_data==NULL) goto fail_3;

    y = malloc(sizeof(real_t*)*(buffer_size+1));
    if(y==NULL) goto fail_4;

    alpha = malloc(sizeof(real_t)*buffer_size);
    if(alpha==NULL) goto fail_5;

    rho = malloc(sizeof(real_t)*buffer_size);
    if(rho==NULL) goto fail_6;

    direction =calloc(sizeof(real_t),DIMENSION_PANOC);
    if(rho==NULL) goto fail_7;

    /*
     * if all the allocations took place, setup the 2D arrays
     */
    unsigned int i;
    for (i = 0; i < buffer_size+1; i++)
    {
        s[i] = s_data + i*DIMENSION_PANOC;
        y[i] = y_data + i*DIMENSION_PANOC;
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
        free(direction);
        active_buffer_size=0;
        return SUCCESS;
}

unsigned int lbfgs_get_active_buffer_size(void){return active_buffer_size;}

int lbfgs_reset_iteration_counters(void){
    active_buffer_size=0;
    hessian_estimate=1;
    return SUCCESS;
}

/*
 * returns the direction calculated with lbfgs
 */ 
const real_t* lbfgs_get_direction(void){
    const real_t* direction_prox_gradient = proximal_gradient_descent_get_buffered_direction();
    
    /* 
     * If the gradient is about zero then this is a fixed point, 
     * set the direct on zero and return.
     */
    if(vector_norm2(direction_prox_gradient,DIMENSION_PANOC)<MACHINE_ACCURACY){
        lbfgs_reset_direction();
        return direction;
    }

    /* is this the first time you call get_direction? */
    if(active_buffer_size==0){
        /* 
         * use gradient descent for first iteration 
         */
        vector_minus(direction_prox_gradient,direction,DIMENSION_PANOC); /* set the direction */
    }else{
        int buffer_limit; /* how much of the buffer should i use in this iteration? */
        if(active_buffer_size<buffer_size){
            buffer_limit=active_buffer_size;
        }else{
            buffer_limit=buffer_size;
        }

        real_t* q = direction; /* use the direction variable temporarily as q */
        vector_copy(direction_prox_gradient,q,DIMENSION_PANOC);

        /*
         * First loop lbfgs
         */
        int i;/*"i" should be able to go negative, as this is used in second loop */
        for (i = 0; i < buffer_limit; i++)
        {
            rho[i] = 1/inner_product(y[i],s[i],DIMENSION_PANOC);
            alpha[i]= rho[i]*inner_product(s[i],q,DIMENSION_PANOC);
            vector_add_ntimes(q,y[i],DIMENSION_PANOC,-alpha[i]);
        }

        real_t* z = direction; /* use the direction variable temporarily as z */
        vector_real_mul(q,DIMENSION_PANOC,hessian_estimate,z);
        /*
         * Second loop lbfgs
         */
        real_t beta;
        for (i = buffer_limit - 1; i >= 0; i--)
        {
            beta=rho[i]*inner_product(y[i],z,DIMENSION_PANOC);
            vector_add_ntimes(z,s[i],DIMENSION_PANOC,(alpha[i]-beta)); 
        }
        vector_minus(z,direction,DIMENSION_PANOC); /* z contains upward direction, multiply with -1 to get downward direction */
    }
    
    return direction;
}
int lbfgs_update_hessian(real_t tau, const real_t* current_location, const real_t* new_location){
    vector_sub(new_location,current_location,DIMENSION_PANOC,s[buffer_size]); /* set s */
    
    real_t gradient_current_location[DIMENSION_PANOC];proximal_gradient_descent_get_current_residual(gradient_current_location);

    real_t gradient_new_location[DIMENSION_PANOC];
    if(tau==0){
        /* direction was never used to calculate forward backward envelop */
        proximal_gradient_descent_get_new_residual(new_location,gradient_new_location);
    }else{
        /* direction was used to calculate forward backward envelop */
        proximal_gradient_descent_get_new_residual_buffered(gradient_new_location);
    }
    
    vector_sub(gradient_new_location,gradient_current_location,DIMENSION_PANOC,y[buffer_size]); /* set y=df(new_x) - df(x) */

    /* scale gamma, this is done in ForBes , but not correct according to paper */
    real_t gamma = proximal_gradient_descent_get_gamma();
    vector_real_mul(y[buffer_size],DIMENSION_PANOC,gamma,y[buffer_size]);

    if(check_if_valid_update(gradient_current_location)==SUCCESS){
        shift_s_and_y();  /* shift the s and y buffers */

        real_t inner_product_sy = inner_product(s[0],y[0],DIMENSION_PANOC);
        real_t inner_product_yy = inner_product(y[0],y[0],DIMENSION_PANOC);
        hessian_estimate=inner_product_sy/inner_product_yy;

        
        active_buffer_size++;

        return SUCCESS;
    }else{
        /* 
         * Update is not valid, return direction but don't save y and s,
         * which means that the hessian approximation stays the sam.
         */
        return FAILURE;
    }    
}
/*
 * Theoretical condition:
 * update if (y^Ts)/||s||^2 > epsilon * ||grad(x)||
 * 
 */
static int check_if_valid_update(const real_t* gradient_current_location){
    /* 
     * The most recent s/y vectors are at the last element of the buffer
     */
    const real_t* possible_s = s[buffer_size];
    const real_t* possible_y = y[buffer_size];

    const real_t inner_product_ys = inner_product(possible_y,possible_s,DIMENSION_PANOC);
    const real_t norm_s = inner_product(possible_s,possible_s,DIMENSION_PANOC);
    const real_t norm_gradient_current_location = vector_norm2(gradient_current_location,DIMENSION_PANOC);

    if(inner_product_ys/norm_s < (1e-12)*norm_gradient_current_location)
        return FAILURE; /* don't update */

    return SUCCESS;
}

 /* internal function used to shift the s and y buffers */
static void shift_s_and_y(void){
        real_t* buffer_s =s[buffer_size];
        real_t* buffer_y =y[buffer_size];
        unsigned int i;
        for (i = buffer_size; i >0 ; i--)
        {
            s[i] = s[i-1];
            y[i] = y[i-1];
        }
        s[0]=buffer_s;
        y[0]=buffer_y;
}

static int lbfgs_reset_direction(void){
    unsigned int i;
    for ( i = 0; i < DIMENSION_PANOC; i++)
    {
        direction[i]=0;
    }
    return SUCCESS;
}