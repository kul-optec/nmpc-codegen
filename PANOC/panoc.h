#ifndef PANOC_H
#define PANOC_H

#include<stddef.h>
#include"../globals/globals.h"

int panoc_init(size_t dimension_,\
    real_t (*g_)(const real_t* input),\
    void (*proxg_)(const real_t* input, real_t* output),\
    real_t (*f_)(const real_t* input),\
    void (*df_)(const real_t* input, real_t* output));
int panoc_cleanup();

int panoc_get_new_location(const real_t* current_state,real_t* optimal_inputs);

real_t panoc_get_tau(void);
#endif