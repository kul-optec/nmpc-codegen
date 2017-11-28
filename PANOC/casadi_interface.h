#ifndef CASADI_INTERFACE_H
#define CASADI_INTERFACE_H

#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

typedef struct {
    int inputSize;
    int outputSize;
    int buffer_intSize;
    int buffer_realSize;
    int* buffer_int;
    real_t* buffer_real;
    int (*cost_function)(const real_t** arg, real_t** res, int* iw, real_t* w, int mem);
} CasadiFunction;

int casadi_interface_init();
int casadi_interface_cleanup();
int casadi_set_state(const real_t* current_state);
size_t casadi_interface_get_dimension();

/* cost functions */
real_t casadi_interface_f(const real_t* input);
void casadi_interface_df(const real_t* input,real_t* output);
real_t casadi_interface_g(const real_t* input);
void casadi_interface_proxg(const real_t* input,real_t* output);

#endif