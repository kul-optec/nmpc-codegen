#include"lipschitz.h"
#include"matrix_operations.h"
#include"math.h"
#include"casadi_interface.h"
#include <stddef.h>
#include <stdlib.h>
#include "buffer.h"
/*
 * Get the step used to estimate the lipschitz constant
 * delta= max{small number,10^{-6}*u_0}
 */
real_t get_lipschitz_get_delta(const real_t* current_position){
    real_t safety_value_delta = vector_norm2(current_position,casadi_interface_get_dimension())*DELTA_LIPSCHITZ_SAFETY_VALUE;
    if(DELTA_LIPSCHITZ>safety_value_delta)
        return DELTA_LIPSCHITZ;
    else return safety_value_delta;
}
/*
 * Estimate the lipschitz constant by using the numerical hessian as an estimation
 * Theorem:
 *     ||gradient(x)|| < B
 *     f is B-lipschitz
 */
real_t get_lipschitz(const real_t* current_position){
    const size_t dimension=casadi_interface_get_dimension();
    const real_t delta=get_lipschitz_get_delta(current_position);

    real_t current_position_delta[dimension];
    real_t df_current_position_delta[dimension];

    /* copy over the current position and add delta*/
    vector_real_add(current_position,dimension,delta,current_position_delta);

    /* calculate the two gradients and save them in the same variable */
    const real_t* df_current_position=buffer_get_current_df();
    casadi_interface_f_df(current_position_delta,df_current_position_delta);

    /* 
     * L = norm((df(x+delta)-df(x))/delta) 
     * reuse the current_position_delta values as buffer
     */
    vector_sub(df_current_position,df_current_position_delta,dimension,current_position_delta); /* step1: df(x+delta)-df(x) */
    const real_t numerator = vector_norm2(current_position_delta,dimension); /* step2: norm((df(x+delta)-df(x))) */
    const real_t denominator = sqrt(dimension)*delta; /* step3: norm(current_position_delta) */

    return numerator/denominator;
}