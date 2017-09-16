#ifndef LBFGS_H
#define LBFGS_H

#include "../globals/globals.h"

int lbfgs_init();
int lbfgs_cleanup();

/*
 * returns the direction calculated with lbfgs
 */ 
 int lbfgs_get_direction(real_t* current_location,real_t* direction);

#endif 