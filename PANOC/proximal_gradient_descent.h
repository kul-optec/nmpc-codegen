#ifndef PROXIMAL_GRADIENT_DESCENT_H
#define PROXIMAL_GRADIENT_DESCENT_H

#include"../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

int proximal_gradient_descent_init(void);
int proximal_gradient_descent_cleanup(void);
const real_t* proximal_gradient_descent_get_direction(void);

/*
 * Reset iteration index and gamma, call me if your starting with a new problem
 */
int proximal_gradient_descent_reset_iteration_counters(void);

/*
 * calculate the forward backward envelop using the internal gamma
 * Matlab cache.FBE = cache.fx + cache.gz - cache.gradfx(:)'*cache.FPR(:) + (0.5/gam)*(cache.normFPR^2);
 */
real_t proximal_gradient_descent_forward_backward_envelop(const real_t* location);

/* 
 * Calculate the residual at current_location from the buffer, also precompute the FBE
 * -> the precomputed FBE can be acesed with .._get_current_forward_backward_envelop function
 */
int proximal_gradient_descent_get_current_residual(real_t* residual);
/* 
 * Calculate the residual at a certain location, also precompute FBE 
 * -> the precomputed FBE can be acesed with .._get_lbfgs_forward_backward_envelop
 */
int proximal_gradient_descent_get_residual(const real_t* input,real_t* output);

/* 
 * returns the linesearch parameter or 1/Lipschitz of the gradient
 */
real_t proximal_gradient_descent_get_gamma(void);
/* 
 * returns the residual from the current proximal gradient step 
 */
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