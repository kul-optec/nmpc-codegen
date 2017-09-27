#ifndef LBFGS_H
#define LBFGS_H

#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

int lbfgs_init(size_t buffer_size_,size_t dimension_, \
    void (*gradient_)(real_t* input,real_t* output));
int lbfgs_cleanup(void);

/*
 * returns the direction calculated with lbfgs
 */ 
 int lbfgs_get_direction(real_t* current_location,real_t* direction);

#endif 