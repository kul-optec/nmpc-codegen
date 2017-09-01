#ifndef INTERFACE_CASADI_H
#define INTERFACE_CASADI_H

#include<stdlib.h> 
#include"../globals/globals.h"

int func(const real_t* input,real_t* output);
int init_func();
int cleanup_func();

int get_inputSize();
int get_outputSize();

typedef struct {
    int inputSize;
    int outputSize;
    int buffer_intSize;
    int buffer_realSize;
    int* buffer_int;
    real_t* buffer_real;
} CasadiFunction;

#endif