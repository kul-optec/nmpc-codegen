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
#ifdef INTEGRATOR_CASADI
static CasadiFunction* integrator_data;
#endif

int casadi_interface_init(){
    cost_function_data=init_buffer_casadi_function(cost_function,cost_function_work);
    if(cost_function_data==NULL) goto fail_1;

    cost_function_derivative_combined_data=init_buffer_casadi_function(cost_function_derivative_combined,cost_function_derivative_combined_work);
    if(cost_function_derivative_combined_data==NULL) goto fail_2;

    #ifdef INTEGRATOR_CASADI
        integrator_data=init_buffer_casadi_function(integrator,integrator_work);
        if(integrator_data==NULL) goto fail_3;
    #endif

    return SUCCESS;

    #ifdef INTEGRATOR_CASADI
    fail_3:
        cleanup_buffer_casadi_function(cost_function_derivative_combined_data);
    #endif
    fail_2:
        cleanup_buffer_casadi_function(cost_function_data);
    fail_1:
        return FAILURE;
}
int casadi_interface_cleanup(){
    cleanup_buffer_casadi_function(cost_function_data);
    cleanup_buffer_casadi_function(cost_function_derivative_combined_data);
    #ifdef INTEGRATOR_CASADI
    cleanup_buffer_casadi_function(integrator_data);
    #endif
    return SUCCESS;
}
#ifdef INTEGRATOR_CASADI
int casadi_integrate(const real_t* current_state,const real_t* input,real_t* new_state){
    const real_t* input_casadi[2]={current_state,input};
    real_t* output_casadi[1]={new_state};

    integrator_data->cost_function(input_casadi,output_casadi,\
        integrator_data->buffer_int,\
        integrator_data->buffer_real,\
        MEM_CASADI);

    return SUCCESS;
}
#endif
static const real_t* state;
int casadi_set_state(const real_t* current_state){
    state = current_state;
    return SUCCESS;
}
size_t casadi_interface_get_dimension(){
    return DIMENSION_INPUT*MPC_HORIZON;
}

/* cost functions */
real_t casadi_interface_f(const real_t* input){
    real_t data_output;
    real_t* output[1] = {&data_output};

    const real_t* input_function[2]={state,input};

    cost_function_data->cost_function(input_function,output,\
        cost_function_data->buffer_int,\
        cost_function_data->buffer_real,\
        MEM_CASADI);

    return *output[0];
}

real_t casadi_interface_f_df(const real_t* input,real_t* data_output){
    real_t f_value;
    real_t* output[2] = {&f_value,data_output};
    const real_t* input_function[2]={state,input};

    cost_function_derivative_combined_data->cost_function(input_function,output,\
        cost_function_derivative_combined_data->buffer_int,\
        cost_function_derivative_combined_data->buffer_real,\
        MEM_CASADI);
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