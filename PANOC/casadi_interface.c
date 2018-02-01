#include "../globals/globals.h"

#include "casadi_definitions.h"

#include "../casadi/cost_function.c"
#include "../casadi/cost_function_derivative_combined.c"

#include <stddef.h>
#include <stdlib.h>
#include "casadi_interface.h"

#include "../casadi/g.c"
#include "../casadi/proxg.c"
#ifdef INTEGRATOR_CASADI
#include "../casadi/integrator.c"
#endif

CasadiFunction* init_buffer_casadi_function( \
        int (*cost_function)(const real_t** arg, real_t** res, int* iw, real_t* w, int mem),  \
        int (*work_array_size)(int*, int*, int *, int *)\
        );
int cleanup_buffer_casadi_function(CasadiFunction* data);

static CasadiFunction* cost_function_data;
static CasadiFunction* cost_function_derivative_combined_data;
static real_t* obstacle_weights;
#ifdef INTEGRATOR_CASADI
static CasadiFunction* integrator_data;
#endif

int casadi_interface_init(){
    if(NUMBER_OF_OBSTACLES>0){
        obstacle_weights=malloc(sizeof(real_t)*NUMBER_OF_OBSTACLES);
        if(obstacle_weights==NULL) goto fail_1;
        else{
            size_t i;
            for (i = 0; i < NUMBER_OF_OBSTACLES; i++)
            {
                obstacle_weights[i]=DEFAULT_OBSTACLE_WEIGHT;
            }
        }
    }
    return SUCCESS;

    fail_1:
        return FAILURE;
}
int casadi_interface_cleanup(){
    free(obstacle_weights);
    return SUCCESS;
}
#ifdef INTEGRATOR_CASADI
int casadi_integrate(const real_t* current_state,const real_t* input,real_t* new_state){
    const real_t* input_casadi[2]={current_state,input};
    real_t* output_casadi[1]={new_state};

    return integrator(input_casadi, output_casadi, NULL, NULL, MEM_CASADI);

    /* old code, the arrays are unused this way
    integrator_data->cost_function(input_casadi,output_casadi,\
        integrator_data->buffer_int,\
        integrator_data->buffer_real,\
        MEM_CASADI);
    */
}
#endif
static const real_t* state;
static const real_t* state_reference;
static const real_t* input_reference;
int casadi_prepare_cost_function(   const real_t* _current_state,
                                    const real_t* _state_reference,
                                    const real_t* _input_reference){
    state = _current_state;
    state_reference=_state_reference;
    input_reference=_input_reference;
    return SUCCESS;
}
size_t casadi_interface_get_dimension(){
    return DIMENSION_PANOC;
}

/* cost functions */
real_t casadi_interface_f(const real_t* input){
    real_t data_output;
    real_t* output[1] = {&data_output};

    const real_t* input_function[5]={state,input,state_reference,input_reference,obstacle_weights};

    cost_function(input_function, output, NULL, NULL, MEM_CASADI);

    /* old code, the arrays are unused this way
    cost_function_data->cost_function(input_function,output,\
        cost_function_data->buffer_int,\
        cost_function_data->buffer_real,\
        MEM_CASADI);
    */
    return *output[0];
}

real_t casadi_interface_f_df(const real_t* input,real_t* data_output){
    real_t f_value;
    real_t* output[2] = {&f_value,data_output};
    const real_t* input_function[5]={state,input,state_reference,input_reference,obstacle_weights};

    cost_function_derivative_combined(input_function, output, NULL, NULL, MEM_CASADI);

    /* old code, the arrays are unused this way
    cost_function_derivative_combined_data->cost_function(input_function,output,\
        cost_function_derivative_combined_data->buffer_int,\
        cost_function_derivative_combined_data->buffer_real,\
        MEM_CASADI);
    */
    return f_value;
}


int cleanup_buffer_casadi_function(CasadiFunction* data){
    free(data->buffer_int);
    free(data->buffer_real);
    free(data);
    return SUCCESS; 
}

CasadiFunction* init_buffer_casadi_function( \
        int (*cost_function)(const real_t** arg, real_t** res, int* iw, real_t* w, int mem),  \
        int (*work_array_size)(int*, int*, int *, int *) \
        ){

    CasadiFunction* function_data = malloc(sizeof(CasadiFunction));
    if(function_data==NULL) goto fail_function_data;

    /* 
     * get the proper sizes trough the work function, 
     * ignore the return value as its always zero 
     */
    work_array_size(&function_data->inputSize,&function_data->outputSize,&function_data->buffer_intSize,&function_data->buffer_realSize);
    function_data->cost_function=cost_function;
    /* 
     * Allocate the buffers.
     */
    function_data->buffer_int = malloc(sizeof(int)*function_data->buffer_intSize);
    if(function_data->buffer_int==NULL) goto fail_buffer_int;
    function_data->buffer_real = malloc(sizeof(real_t)*function_data->buffer_realSize);
    if(function_data->buffer_real==NULL) goto fail_buffer_real;

    /* 
     * if all the allocations took place, return data
     */
    return function_data;

    /*
     * something went wrong free up the necessary memory and return failure
     */
    fail_buffer_real: 
        free(function_data->buffer_int);
    fail_buffer_int:
        free(function_data->buffer_real);
    fail_function_data: 
        return NULL;
}

real_t casadi_get_weight_obstacles(int index_obstacle){
    if(index_obstacle<NUMBER_OF_OBSTACLES && index_obstacle>=0)return obstacle_weights[index_obstacle];
    return 0;
}
int casadi_set_weight_obstacles(int index_obstacle,real_t weight){
    if(index_obstacle<NUMBER_OF_OBSTACLES && index_obstacle>=0){
        obstacle_weights[index_obstacle]=weight;
        return SUCCESS;
    }
    return FAILURE;
}