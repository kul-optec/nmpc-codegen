#ifndef CASADI_DEFINITIONS_H
#define CASADI_DEFINITIONS_H

#include"../globals/globals.h"

#define to_double(x) (double) x
#define to_int(x) (int) x
#define CASADI_CAST(x,y) (x) y

/* Pre-c99 compatibility */
#if __STDC_VERSION__ < 199901L
    real_t fmin(real_t x, real_t y) { return x<y ? x : y;}
    real_t fmax(real_t x, real_t y) { return x>y ? x : y;}
#endif

real_t sq(real_t x) { return x*x;}
real_t sign(real_t x) { return x<0 ? -1 : x>0 ? 1 : x;}

#endif