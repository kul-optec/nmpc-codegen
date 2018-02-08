#include<stdlib.h>
#include"lbfgs.h"
#include"../globals/globals.h"
#include"../include/nmpc.h"
#include "panoc.c"
#include "casadi_interface.h"
#include "math.h"

static real_t* current_input;
static real_t* new_input;

int nmpc_init(void){
    int dimension = casadi_interface_get_dimension();
    if(panoc_init()==FAILURE) goto fail_1;
    current_input=calloc(dimension,sizeof(real_t)); /* start with the zero input */
    if(current_input==NULL) goto fail_2;
    new_input=malloc(dimension*sizeof(real_t));
    if(new_input==NULL) goto fail_3;
    if(casadi_interface_init()==FAILURE) goto fail_4;

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
int nmpc_cleanup(void){
    panoc_cleanup();
    free(current_input);
    free(new_input);
    return SUCCESS;
}
static void switch_input_current_new(void){
    real_t* buffer;
    buffer=current_input;
    current_input=new_input;
    new_input=buffer;
}
int npmc_solve( const real_t* current_state,
                const real_t* state_reference,
                const real_t* input_reference,
                real_t* optimal_inputs){ 
    casadi_prepare_cost_function(current_state,state_reference,input_reference);

    /* 
     * take implicitly the previous inputs as the starting position for the algorithm 
     */
    
    int i_panoc;
    real_t residual=1;
    for (i_panoc= 0; i_panoc < PANOC_MAX_STEPS ; i_panoc++)
    {
        if(i_panoc > PANOC_MIN_STEPS && residual<MIN_RESIDUAL){
            /* if more then PANOC_MIN_STEPS steps are passed 
               and residual is low stop iterating */
            break;
        }
        residual = panoc_get_new_location(current_input,new_input);

        /* set the new_input as input for the next iteration */
        switch_input_current_new();
    }
    /* only return the optimal input */
    int i;
    for (i = 0; i < DIMENSION_INPUT; i++)
    {
        optimal_inputs[i]=current_input[i];
    }
    panoc_reset_cycli();
    if(i_panoc==PANOC_MAX_STEPS)
        return i_panoc;
    return i_panoc-1;
}
int nmpc_get_last_full_solution(real_t* output){
    int i;
    int dimension = casadi_interface_get_dimension();
    for ( i = 0; i < dimension ; i++)
    {
        output[i]=current_input[i];
    }
    return SUCCESS;
}

real_t nmpc_get_weight_obstacles(int index_obstacle){
    return casadi_get_weight_obstacles(index_obstacle);
}
int nmpc_set_weight_obstacles(int index_obstacle,real_t weight){
    return casadi_set_weight_obstacles(index_obstacle,weight);
}
int nmpc_set_buffer_solution(real_t value, int index){
    current_input[index]=value;
    return SUCCESS;
}