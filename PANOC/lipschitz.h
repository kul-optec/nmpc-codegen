#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

#ifndef LIPSCHITZ_H
#define LIPSCHITZ_H

real_t get_lipschitz(void (*gradient)(const real_t*,real_t*),const real_t* current_position,const size_t dimension);

#endif