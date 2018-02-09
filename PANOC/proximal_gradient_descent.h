#ifndef PROXIMAL_GRADIENT_DESCENT_H
#define PROXIMAL_GRADIENT_DESCENT_H

#include"../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

int proximal_gradient_descent_init(void);
int proximal_gradient_descent_reset_iteration_counters(void);
int proximal_gradient_descent_cleanup(void);
const real_t* proximal_gradient_descent_get_direction(void);

/*
 * calculate the forward backward envelop using the internal gamma
 * Matlab cache.FBE = cache.fx + cache.gz - cache.gradfx(:)'*cache.FPR(:) + (0.5/gam)*(cache.normFPR^2);
 */
real_t proximal_gradient_descent_forward_backward_envelop(const real_t* location);

/*
 * function with lbgfs
 */
int proximal_gradient_descent_get_residual(const real_t* input,real_t* output);
int proximal_gradient_descent_get_current_residual(real_t* residual);

real_t proximal_gradient_descent_get_gamma(void);
real_t proximal_gradient_descent_get_current_residual_inf_norm(void);

/*
 * return the precomputed forward backward envelop of the current location
 */
real_t proximal_gradient_descent_get_current_forward_backward_envelop(void);
/*
 * return the precomputed forward backward envelop of a pure lbfgs step (tau=1)
 */
real_t proximal_gradient_descent_get_lbfgs_forward_backward_envelop(void);

#endif // !PROXIMAL_GRADIENT_DESCENT_H