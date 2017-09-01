#ifndef PANOC_H
#define PANOC_H

#include<stddef.h>
#include"../globals/globals.h"

int panoc_init();
int panoc_cleanup();

int panoc_solve(real_t* current_state,real_t* optimal_inputs);
#endif