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
    
    if(casadi_interface_init()) goto fail_4;

    return SUCCESS;
    fail_4:
        casadi_interface_cleanup();
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
void switch_input_current_new(){
    real_t* buffer;
    buffer=current_input;
    current_input=new_input;
    new_input=buffer;

}
int npmc_solve(const real_t* current_state,real_t* optimal_inputs){
    casadi_set_state(current_state);

    /* 
     * take implicityly the previous inputs as the starting position for the algorithm 
     */

    size_t i;
    for (i= 0; i < PANOC_MAX_STEPS; i++)
    {
        panoc_get_new_location(current_input,new_input);

        /* set the new_input as input for the next iteration */
        switch_input_current_new();
    }
    /* only return the optimal input */
    for (i = 0; i < DIMENSION_INPUT; i++)
    {
        optimal_inputs[i]=current_input[i];
    }
    panoc_reset_cycli();
    return SUCCESS;
}