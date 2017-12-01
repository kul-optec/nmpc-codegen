#ifndef NMPC_H
#define NMPC_H

#include<stdlib.h>

int nmpc_init();
int nmpc_cleanup();
int npmc_solve(const real_t* current_state,real_t* optimal_inputs);

#endif