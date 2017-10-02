#ifndef CASADI_INTERFACE_H
#define CASADI_INTERFACE_H

#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

int casadi_interface_init(const real_t* current_state);
size_t casadi_interface_get_dimension();

/* cost functions */
real_t casadi_interface_f(const real_t* input);
void casadi_interface_df(const real_t* input,real_t* output);
real_t casadi_interface_g(const real_t* input);
void casadi_interface_proxg(const real_t* input,real_t* output);

#endif