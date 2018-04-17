#include "../globals/globals.h"

#include "../casadi/cost_function_derivative_combined.h"

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

static real_t* constraint_weights;
static const real_t* state;

#ifdef INTEGRATOR_CASADI
/* static CasadiFunction* integrator_data; */
#endif

int casadi_interface_init(){
    if(NUMBER_OF_CONSTRAINTS>0){
        constraint_weights=malloc(sizeof(real_t)*NUMBER_OF_CONSTRAINTS);
        if(constraint_weights==NULL) goto fail_1;
        else{
            size_t i;
            for (i = 0; i < NUMBER_OF_CONSTRAINTS; i++)
            {
                constraint_weights[i]=DEFAULT_CONSTRAINT_WEIGHT;
            }
        }
    }
    return SUCCESS;

    fail_1:
        return FAILURE;
}
int casadi_interface_cleanup(){
    free(constraint_weights);
    return SUCCESS;
}
#ifdef INTEGRATOR_CASADI
int casadi_integrate(const real_t* current_state,const real_t* input,real_t* new_state){
    const real_t* input_casadi[2]={current_state,input};
    real_t* output_casadi[1]={new_state};

    return integrator(input_casadi, output_casadi, NULL, NULL, MEM_CASADI);
}
#endif

/*  
 * Function only used when using lagrangian
 */
#ifdef USE_LA
int casadi_evaluate_constraints(const real_t* inputs,real_t* constraint_values){
    const real_t* input_casadi[2]={state,inputs};
    real_t* output_casadi[1]={constraint_values};

    evaluate_constraints(input_casadi, output_casadi, NULL, NULL, MEM_CASADI);
    return SUCCESS;
}
#endif

int casadi_prepare_cost_function(const real_t* _current_state){
    state = _current_state;
    return SUCCESS;
}

/* cost functions */
#ifndef SINGLE_COST_MODE
#include "../casadi/cost_function.h"
real_t casadi_interface_f(const real_t* input){
    real_t data_output;
    real_t* output[1] = {&data_output};

    const real_t* input_function[3]={state,input,constraint_weights};

    cost_function(input_function, output, NULL, NULL, MEM_CASADI);

    return *output[0];
}
#endif

real_t casadi_interface_f_df(const real_t* input,real_t* data_output){
    real_t f_value;
    real_t* output[2] = {&f_value,data_output};
    const real_t* input_function[3]={state,input,constraint_weights};

    cost_function_derivative_combined(input_function, output, NULL, NULL, MEM_CASADI);

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

real_t casadi_get_weight_constraints(int index_constraint){
    if(index_constraint<NUMBER_OF_CONSTRAINTS && index_constraint>=0)return constraint_weights[index_constraint];
    return 0;
}
int casadi_set_weight_constraints(int index_constraint,real_t weight){
    if(index_constraint<NUMBER_OF_CONSTRAINTS && index_constraint>=0){
        constraint_weights[index_constraint]=weight;
        return SUCCESS;
    }
    return FAILURE;
}