#include"lipschitz.h"
#include"matrix_operations.h"
#include"math.h"

/*
 * Estimate the lipschitz constant by using the numerical hessian as an estimation
 * Theorem:
 *     ||gradient(x)|| < B
 *     f is B-lipschitz
 */
real_t estimate_lipschitz(void (*gradient)(real_t*), real_t* current_position,const size_t size_current_position){
    real_t current_position_delta[size_current_position];

    /* copy over the current position and add delta*/
    VECTOR_REAL_ADD(current_position,size_current_position,delta_lipschitz,current_position_delta);

    /* calculate the two gradients and save them in the same variable */
    gradient(current_position);
    gradient(current_position_delta);

    /* substract the 2 vectors */
    VECTOR_SUB(current_position,current_position_delta,current_position,size_current_position)

    real_t norm2_delta = sqrt(pow(delta_lipschitz,2)*size_current_position);
    return norm2_vector(current_position,size_current_position)/norm2_delta;
}