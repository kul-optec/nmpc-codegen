#ifndef EXAMPLE_PROBLEMS_H
#define EXAMPLE_PROBLEMS_H

#include "../../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

int example_problems_set_init_problem1(real_t w,size_t dimension);
real_t g_1(const real_t* x);
void proxg_1(const real_t* x ,real_t* proxg_x);

#endif