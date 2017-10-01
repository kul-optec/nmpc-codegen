#ifndef PROXIMAL_GRADIENT_DESCENT_H
#define PROXIMAL_GRADIENT_DESCENT_H

#include"../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

int proximal_gradient_descent_init(size_t dimension, \
    real_t (*g_)(const real_t* input), \
    void (*proxg_)(const real_t* input, real_t* output),\
    real_t (*f_)(const real_t* input),\
    void (*df_)(const real_t* input, real_t* output));
int proximal_gradient_descent_cleanup(void);
const real_t* proximal_gradient_descent_get_direction(const real_t* current_location);

/*
 * calculate the forward backward envelop using the internal gamma
 * Matlab cache.FBE = cache.fx + cache.gz - cache.gradfx(:)'*cache.FPR(:) + (0.5/gam)*(cache.normFPR^2);
 */
real_t proximal_gradient_descent_forward_backward_envelop(const real_t* current_location);

/*
 * function with lbgfs
 */
int proximal_gradient_descent_get_residual(const real_t* input,real_t* output);
real_t proximal_gradient_descent_get_gamma(void);

#endif // !PROXIMAL_GRADIENT_DESCENT_H