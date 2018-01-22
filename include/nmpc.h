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
const real_t* nmpc_get_last_full_solution(void);

#endif