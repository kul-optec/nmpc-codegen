#include"panoc.h"
#include<stdlib.h>
#include"lbfgs.h"
#include"proximal_gradient_descent.h"
#include"matrix_operations.h"
#include"../globals/globals.h"

real_t (*g)(const real_t* input);
void (*proxg)(const real_t* input, real_t* output);
real_t (*f)(const real_t* input);
void (*df)(const real_t* input, real_t* output);

/* variables set once by init */
static size_t dimension;

/* variables reused by each get direction */
static real_t tau;
static real_t FBE_current_location;
static real_t direction_norm;

/* functions used internally */
int panoc_check_linesearch_condition(const real_t* current_location, real_t* new_location, const real_t sigma);
int panoc_get_new_potential_location(const real_t* current_location ,const  real_t* forward_backward_step,
    const real_t* direction_residue,const real_t tau,real_t* potential_new_location);

/*
 * Initialize the panoc library
 * This function should allways be called before doing anything with the panoc lib
 */
int panoc_init(size_t dimension_,\
        real_t (*g_)(const real_t* input),\
        void (*proxg_)(const real_t* input, real_t* output),\
        real_t (*f_)(const real_t* input),\
        void (*df_)(const real_t* input, real_t* output)){
    dimension=dimension_;
    g=g_;f=f_;proxg=proxg_;df=df_;

    if(lbfgs_init(LBGFS_BUFFER_SIZE,dimension)==FAILURE) goto fail_1;
    if(proximal_gradient_descent_init(dimension,g,proxg,f,df)==FAILURE) goto fail_2;

    return SUCCESS;

    fail_2:
        lbfgs_cleanup();
    fail_1:
        return FAILURE;
}

/*
 * cleanup the panoc library
 * This function cleans up the memory used by the panoc algorithm, 
 * use this when you don't need the lib anymore
 */
int panoc_cleanup(){
    proximal_gradient_descent_cleanup();
    lbfgs_cleanup();
    return SUCCESS;
}

/*
 * Solve the actually MPC problem, return the optimal inputs
 */
int panoc_get_new_location(const real_t* current_location,real_t* new_location){   
    const real_t* forward_backward_step = proximal_gradient_descent_get_direction(current_location);
    const real_t sigma = PROXIMAL_GRAD_DESC_SAFETY_VALUE/(4*proximal_gradient_descent_get_gamma());

    const real_t* direction_residue = lbfgs_get_direction(current_location);

    /* precompute FBE used in linesearch check */
    FBE_current_location = proximal_gradient_descent_forward_backward_envelop(current_location);
    direction_norm=pow(vector_norm2(forward_backward_step,dimension),2);

    tau=1;
    panoc_get_new_potential_location(current_location,forward_backward_step,direction_residue,tau,new_location);
    while(panoc_check_linesearch_condition(current_location,new_location,sigma)==FAILURE){
            tau=tau/2;
            panoc_get_new_potential_location(current_location,forward_backward_step,direction_residue,tau,new_location);
    }
    return SUCCESS;
}

int panoc_check_linesearch_condition(const real_t* current_location, real_t* new_location,const real_t sigma){
    const real_t FBE_potential_new_location = proximal_gradient_descent_forward_backward_envelop(new_location);

    if(FBE_potential_new_location<=FBE_current_location-sigma*direction_norm){
        return SUCCESS; 
    }
    return FAILURE;
}

/* find potential new location x=x-(1-tau)*forward_backward_step+tau*direction_residue */
int panoc_get_new_potential_location(const real_t* current_location ,const  real_t* forward_backward_step,
    const real_t* direction_residue,const real_t tau,real_t* potential_new_location){

    vector_add_2_vectors_a_times(current_location,forward_backward_step,direction_residue,dimension,\
        -(1-tau),tau,potential_new_location); 
    return SUCCESS;
}

real_t panoc_get_tau(void){return tau;}