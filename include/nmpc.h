#ifndef NMPC_H
#define NMPC_H

#include<stdlib.h>
#include "../globals/globals.h"

int nmpc_init();
int nmpc_cleanup();
int npmc_solve( const real_t* current_state,
                const real_t* state_reference,
                const real_t* input_reference,
                real_t* optimal_inputs);

#endif