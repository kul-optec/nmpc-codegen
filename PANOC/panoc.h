#ifndef PANOC_H
#define PANOC_H

#include<stddef.h>
#include"../globals/globals.h"

int panoc_init();
int panoc_cleanup();

const real_t panoc_get_new_location(const real_t* current_location,real_t* optimal_inputs);
int panoc_reset_cycli(void);

real_t panoc_get_tau(void);
#endif