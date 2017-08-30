#include "../globals/globals.h"
#ifdef LIPSCHITZ_H
#define LIPSCHITZ_H

real_t estimate_lipschitz(void (*gradient)(real_t));

#endif