#include"../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

#ifndef PROXIMAL_GRADIENT_DESCENT_H
#define PROXIMAL_GRADIENT_DESCENT_H

#ifdef __cplusplus
extern "C" {
#endif

int proximal_gradient_descent_init(void);
int proximal_gradient_descent_cleanup(void);
const real_t* proximal_gradient_descent_get_direction(void);
const real_t* proximal_gradient_descent_get_buffered_direction(void);

/*
 * Reset iteration index and gamma, call me if your starting with a new problem
 */
int proximal_gradient_descent_reset_iteration_counters(void);

/*
 * calculate the forward backward envelope using the internal gamma
 * Matlab cache.FBE = cache.fx + cache.gz - cache.gradfx(:)'*cache.FPR(:) + (0.5/gam)*(cache.normFPR^2);
 */
real_t proximal_gradient_descent_forward_backward_envelope(const real_t* location);
/*
 * return the precomputed forward backward envelope of the current location
 */
real_t proximal_gradient_descent_get_current_forward_backward_envelope(void);

/* 
 * Calculate the residual at current_location from the buffer
 */
int proximal_gradient_descent_get_current_residual(real_t* residual);
/* 
 * Calculate the residual at a certain location
 */
int proximal_gradient_descent_get_new_residual_buffered(real_t* residual);
int proximal_gradient_descent_get_new_residual(const real_t* input,real_t* output);


/* 
 * returns the linesearch parameter or 1/Lipschitz of the gradient
 */
real_t proximal_gradient_descent_get_gamma(void);
/* 
 * returns the residual from the current proximal gradient step 
 */
real_t proximal_gradient_descent_get_current_residual_inf_norm(void);

#ifdef __cplusplus
}
#endif

#endif // !PROXIMAL_GRADIENT_DESCENT_H