#ifndef NMPC_H
#define NMPC_H

#include<stdlib.h>
#include "../globals/globals.h"

int nmpc_init(void);
int nmpc_cleanup(void);
int npmc_solve( const real_t* current_state,
                const real_t* state_reference,
                const real_t* input_reference,
                real_t* optimal_inputs);
int nmpc_get_last_full_solution(real_t* output);

real_t nmpc_get_weight_constraints(int index_constraint);/* returns zero if index was out of range */
int nmpc_set_weight_constraints(int index_constraint,real_t weight);/* returns failure if the index is out of range */
int nmpc_set_buffer_solution(real_t value, int index); /* set the internal value of the input of the cost function */

#endif