#ifndef LBFGS_H
#define LBFGS_H

#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

int lbfgs_init(const size_t buffer_size_,const size_t dimension_);
int lbfgs_cleanup(void);

/*
 * returns the direction calculated with lbfgs
 */ 
const real_t* lbfgs_get_direction();

#endif 