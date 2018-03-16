/*
 * The nmpc library is build using a layered structure:
 * 
 * --------------------------------------------------
 * |  nmpc                                          |
 * | ---------------------------------------------- |
 * | |                  panoc                     | |
 * | ---------------------------------------------- |
 * | |  proximal gradient  |     lbgfs            | |
 * | ---------------------------------------------- |
 * | |  casadi  | buffer   | lipschitz estimator  | |
 * | ---------------------------------------------- |
 * --------------------------------------------------
 * 
 */

#include<stdlib.h>
#include"lbfgs.h"
#include"../globals/globals.h"
#include"../include/nmpc.h"
#include "panoc.c"
#include "casadi_interface.h"
#include "math.h"

static real_t* current_input;
static real_t* new_input;

static int nmpc_prepare(real_t* static_casadi_parameters,const real_t* current_state,const real_t* state_reference,\
        const real_t* input_reference,const real_t* optimal_inputs);
static int nmpc_solve_classic_way(void);
static int nmpc_solve_with_lagrangian(void);

int nmpc_init(void){
    if(panoc_init()==FAILURE) goto fail_1;
    current_input=calloc(DIMENSION_PANOC,sizeof(real_t)); /* start with the zero input */
    if(current_input==NULL) goto fail_2;
    new_input=malloc(DIMENSION_PANOC*sizeof(real_t));
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
static int nmpc_prepare(real_t* static_casadi_parameters,const real_t* current_state,const real_t* state_reference,\
        const real_t* input_reference,const real_t* optimal_inputs){
    int i;
    for(i=0;i<DIMENSION_STATE;i++){
        static_casadi_parameters[i] = current_state[i];
        static_casadi_parameters[i+DIMENSION_STATE] = state_reference[i];
    }
    for(i=0;i<DIMENSION_INPUT;i++){
        static_casadi_parameters[i+2*DIMENSION_STATE] = input_reference[i];
    }
    casadi_prepare_cost_function(static_casadi_parameters);

    return SUCCESS;
}
int npmc_solve( const real_t* current_state,
                const real_t* state_reference,
                const real_t* input_reference,
                real_t* optimal_inputs){
    real_t static_casadi_parameters[2*DIMENSION_STATE+DIMENSION_INPUT];
    nmpc_prepare(static_casadi_parameters,current_state,state_reference,input_reference,optimal_inputs);

    #ifdef USE_LA
        int i_panoc = nmpc_solve_with_lagrangian();
    #else
        int i_panoc = nmpc_solve_classic_way();
    #endif

    /* only return the optimal input */
    int i;
    for (i = 0; i < DIMENSION_INPUT; i++)
    {
        optimal_inputs[i]=current_input[i];
    }
    // for (i = 0; i < DIMENSION_INPUT*MPC_HORIZON - DIMENSION_INPUT; i++)
    // {
    //     current_input[i] = current_input[i+DIMENSION_INPUT];
    // }
    panoc_reset_cycli();

    return i_panoc;
}

/*
 * Solve the nmpc problem directly
 */
static int nmpc_solve_classic_way(void){
    /* 
     * take implicitly the previous inputs as the starting position for the algorithm 
     */
    int i_panoc;
    real_t residual=1;
    for (i_panoc= 0; i_panoc < PANOC_MAX_STEPS ; i_panoc++){
        if(i_panoc > PANOC_MIN_STEPS && residual<MIN_RESIDUAL){
            /* if more then PANOC_MIN_STEPS steps are passed 
               and residual is low stop iterating */
            break;
        }
        residual = panoc_get_new_location(current_input,new_input);

        /*
         * if the residual was larger then the machine accuracy
         * -> set the new_input as input for the next iteration 
         * WARNING: if the residual was smaller then the machine 
         *  accuracy you might get NaN thats why we won't use it
         */
        if(residual>MACHINE_ACCURACY)
            switch_input_current_new();
    }
    return i_panoc;
}

static int nmpc_solve_with_lagrangian(void){
    /* 
     * take implicitly the previous inputs as the starting position for the algorithm 
     */
    int i_panoc;

    return i_panoc;
}

int nmpc_get_last_full_solution(real_t* output){
    int i;
    for ( i = 0; i < DIMENSION_PANOC ; i++)
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