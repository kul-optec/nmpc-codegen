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
static int nmpc_solve_classic_way(real_t minimum_residual);

#ifdef USE_LA
static int nmpc_solve_with_lagrangian(real_t* static_casadi_parameters);
#endif

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
    

    return SUCCESS;
}
int npmc_solve( const real_t* current_state,
                const real_t* state_reference,
                const real_t* input_reference,
                real_t* optimal_inputs){
    
    /*
     * nmpc-codegen has two was of solving an nmpc problem
     *    1. classic way, min cost(x) + h(x) with h(x) as the soft constraint
     *    2. Accelerated lagrangian
     */
    #ifdef USE_LA
        real_t static_casadi_parameters[2*DIMENSION_STATE+DIMENSION_INPUT+NUMBER_OF_OBSTACLES];
        nmpc_prepare(static_casadi_parameters,current_state,state_reference,input_reference,optimal_inputs);
        /*
         * set lambda's to zero
         */
        int j;
        int start_index_lambdas = DIMENSION_STATE*2 + DIMENSION_INPUT;
        for (j = start_index_lambdas; j < start_index_lambdas + NUMBER_OF_OBSTACLES; j++){
            static_casadi_parameters[j]=0;
        }
        casadi_prepare_cost_function(static_casadi_parameters);
        
        int i_panoc = nmpc_solve_with_lagrangian(static_casadi_parameters);
    #else
        real_t static_casadi_parameters[2*DIMENSION_STATE+DIMENSION_INPUT];
        nmpc_prepare(static_casadi_parameters,current_state,state_reference,input_reference,optimal_inputs);
        casadi_prepare_cost_function(static_casadi_parameters);
        int i_panoc = nmpc_solve_classic_way(MIN_RESIDUAL);
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
static int nmpc_solve_classic_way(real_t minimum_residual){
    /* 
     * take implicitly the previous inputs as the starting position for the algorithm 
     */
    int i_panoc;
    real_t residual=1;
    for (i_panoc= 0; i_panoc < PANOC_MAX_STEPS ; i_panoc++){
        if(i_panoc > PANOC_MIN_STEPS && residual<minimum_residual){
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

#ifdef USE_LA
static int nmpc_solve_with_lagrangian(real_t* static_casadi_parameters){
    /* 
     * take implicitly the previous inputs as the starting position for the algorithm 
     */
    int i_panoc=0;int i;
    real_t minimum_residual=0.1;
    for (i = 0; i < 3; i++)
    {
        /*
         * Solve the problem
         */
        i_panoc += nmpc_solve_classic_way(minimum_residual);
        /*
         * evaluate the constrain functions on the entire horizon
         */
        real_t constraint_values[NUMBER_OF_OBSTACLES];
        casadi_evaluate_constraints(current_input,constraint_values);
        /*
         * calculate new lambda's using the following formula:
         *      lambda^{k+1} = lambda^{k} - 2*mu^{k}c^{i}(x^{k})
         * The lambda's are saved in the inputs array at the end,
         * the amount of lambda's is equal to the amount of constraints
         */
        int j;
        for (j=0;j<NUMBER_OF_OBSTACLES;j++){
            real_t weight_constraint = casadi_get_weight_obstacles(j);
            int start_index_lambdas = DIMENSION_STATE*2 + DIMENSION_INPUT;
            static_casadi_parameters[start_index_lambdas+j]=static_casadi_parameters[start_index_lambdas+j] - 2*weight_constraint*constraint_values[j];

            /*
             * calibrate the constraint weights
             */
            //TODO: check value constraint before updating obs weight
            casadi_set_weight_obstacles(j,weight_constraint*10);
        }

        /*
         * lower the residual used in the next iteration
         */
        minimum_residual = minimum_residual/10.;
    }
    /*
     * temporary solution reset weights back to
     */
    int j;
    for (j=0;j<NUMBER_OF_OBSTACLES;j++){
        real_t weight_constraint = casadi_get_weight_obstacles(j);
        casadi_set_weight_obstacles(j,weight_constraint/1000);
    }
    return i_panoc;
}
#endif
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