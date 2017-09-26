/*
 * 
 */
#include"../include/panoc.h"
#include<stdlib.h>

real_t (*g)(real_t* input);
void (*proxg)(real_t* input, real_t* output);
real_t (*f)(real_t* input);
void (*df)(real_t* input, real_t* output);

/* variables set once by init */
static size_t dimension;
static real_t* direction_prox;
static real_t* direction_residue;

/* variables reused by each get direction */
real_t tau;

/* functions used internally */
int panoc_check_linesearch_condition(real_t* current_location, real_t* new_location, real_t sigma);
int panoc_get_new_potential_location(real_t* current_location , real_t* potential_new_location);

/*
 * Initialize the panoc library
 * This function should allways be called before doing anything with the panoc lib
 */
int panoc_init(size_t dimension_,\
        real_t (*g_)(real_t* input),\
        void (*proxg_)(real_t* input, real_t* output),\
        real_t (*f_)(real_t* input),\
        void (*df_)(real_t* input, real_t* output)){
    dimension=dimension_;
    g=g_;f=f_;proxg=proxg_;df=df_;

    direction_prox=malloc(sizeof(real_t*)*dimension);
    if(direction_prox==NULL)goto fail_1;

    direction_residue=malloc(sizeof(real_t*)*dimension);
    if(direction_residue==NULL) goto fail_2;

    return SUCCESS;

    fail_2:
        free(direction_prox);
    fail_1:
        return FAILURE;
}

/*
 * cleanup the panoc library
 * This function cleans up the memory used by the panoc algorithm, 
 * use this when you don't need the lib anymore
 */
int panoc_cleanup(){
    free(direction_prox);
    free(direction_residue);
}

/*
 * Solve the actually MPC problem, return the optimal inputs
 */
int panoc_solve(real_t* current_location,real_t* new_location){
    tau=1;
    real_t sigma = PROXIMAL_GRAD_DESC_SAFETY_VALUE/(4*proximal_gradient_descent_get_gamma());

    real_t direction_prox[dimension];
    proximal_gradient_descent_get_direction(current_location,direction_prox);

    real_t direction_residue[dimension];
    lbfgs_get_direction(current_location,direction_residue);

    panoc_get_new_potential_location(current_location , new_location);
    while(panoc_check_linesearch_condition(current_location,new_location, sigma) ){
            tau=tau/2;
            panoc_get_new_potential_location(current_location , new_location);
    }

    return SUCCESS;
}

int panoc_check_linesearch_condition(real_t* current_location, real_t* new_location, real_t sigma){

    real_t FBE_potential_new_location = proximal_gradient_descent_forward_backward_envelop(new_location);
    real_t FBE_potential_current_location = proximal_gradient_descent_forward_backward_envelop(current_location);

    if(FBE_potential_new_location<=FBE_potential_current_location-sigma*norm2_vector(direction_prox)){
        return SUCCESS; /* condition is not met */
    }
    return FAILURE; /* condition is met */
}

int panoc_get_new_potential_location(real_t* current_location , real_t* potential_new_location){
    vector_add_ntimes(current_location,direction_prox,dimension,-(1-tau),potential_new_location);
    vector_add_ntimes(potential_new_location,direction_residue,dimension,tau,potential_new_location);
    return SUCCESS;
}