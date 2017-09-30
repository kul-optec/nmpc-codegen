#include<stdio.h>
#include"../globals/globals.h"
#include <stdlib.h> 
#include "interfaceCasadi.h"

#include "../casadi/f.c"
/*
 * DOCUMENTATION casadi: http://casadi.sourceforge.net/users_guide/html/node5.html
 */

static CasadiFunction f_data;

/*
 * call this function to evaluate f
 */
int func(const real_t* input,real_t* output){
    // int f(const real_t** arg, real_t** res, int* iw, real_t* w, int mem)
    f(&input,&output,f_data.buffer_int,f_data.buffer_real,MEM_CASADI);
    return SUCCESS;
}

/*
 * call this function before doing anything
 */
int init_func(){
    /* 
     * get the proper sizes trough the work function, 
     * ignore the return value as its always zero 
     */
    f_work(&f_data.inputSize,&f_data.outputSize,&f_data.buffer_intSize,&f_data.buffer_realSize);

    /* 
     * Allocate the buffers.
     */
    f_data.buffer_int = malloc(sizeof(int)*f_data.buffer_intSize);
    if(f_data.buffer_int==NULL) goto fail_buffer_int;
    f_data.buffer_real = malloc(sizeof(real_t)*f_data.buffer_realSize);
    if(f_data.buffer_real==NULL) goto fail_buffer_real;

    /*
     * if all the allocations took place, return success
     */
    return SUCCESS;

    /*
     * something went wrong free up the necessary memory and return failure
     */
    fail_buffer_real: 
        free(f_data.buffer_int);
    fail_buffer_int:
        return FAILURE;
}

/*
 * call this function after your done with everything
 */
int cleanup_func(){
    /* free up the memory used by the buffer */
    free(f_data.buffer_int);
    free(f_data.buffer_real);
    return SUCCESS;
}

/*
 * because the input only contains a single vector 
 * the sparcity parameters are not relevant here
 */
int get_inputSize(){
    return f_data.inputSize;
}
int get_outputSize(){
    return f_data.outputSize;
}