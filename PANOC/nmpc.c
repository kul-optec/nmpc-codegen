#include<stdlib.h>
#include"lbfgs.h"
#include"../globals/globals.h"
#include"../include/nmpc.h"
#include "panoc.c"
#include "casadi_interface.h"

static real_t* current_input;
static real_t* new_input;

int nmpc_init(){
    if(panoc_init()==FAILURE) goto fail_1;
    current_input=calloc(DIMENSION_INPUT*MPC_HORIZON,sizeof(real_t)); /* start with the zero input */
    if(current_input==NULL) goto fail_2;
    new_input=malloc(DIMENSION_INPUT*MPC_HORIZON*sizeof(real_t));
    if(new_input==NULL) goto fail_3;

    return SUCCESS;
    fail_3:
        free(current_input);
    fail_2:
        panoc_cleanup();
    fail_1:
        return FAILURE;
}
int nmpc_cleanup(){
    panoc_cleanup();
    free(current_input);
    free(new_input);
    return SUCCESS;
}
int npmc_solve(const real_t* current_state,real_t* optimal_inputs){
    casadi_set_state(current_state);
    
    size_t i;
    for (i= 0; i < PANOC_MAX_STEPS; i++)
    {
        panoc_get_new_location(current_input,new_input);

        /* set the new_input as input for the next iteration */
        real_t* buffer;
        buffer=current_input;
        current_input=new_input;
        new_input=buffer;

    }
    /* only return the optimal input */
    for (i = 0; i < DIMENSION_INPUT; i++)
    {
        optimal_inputs[i]=current_input[i];
    }
    return SUCCESS;
}