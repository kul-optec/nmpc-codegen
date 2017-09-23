#ifndef PROXIMAL_GRADIENT_DESCENT_H
#define PROXIMAL_GRADIENT_DESCENT_H

#include"../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

int proximal_gradient_descent_init(size_t dimension, \
    void (*proxg_)(real_t* input, real_t* output),\
    real_t (*f_)(real_t* input),\
    void (*df_)(real_t* input, real_t* output));
int proximal_gradient_descent_cleanup(void);
int proximal_gradient_descent_get_direction(real_t* current_location,real_t* direction);

/*
 * function with lbgfs
 */
int proximal_gradient_descent_get_residue(real_t* input,real_t* output);
real_t proximal_gradient_descent_get_gamma(void);

#endif // !PROXIMAL_GRADIENT_DESCENT_H