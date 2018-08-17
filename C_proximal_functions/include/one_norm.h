#ifndef ONE_NORM_H
#define ONE_NORM_H

#include "../globals/globals.h"

struct one_norm{
    real_t mu;
    unsigned int dimension;
};

struct one_norm* init_one_norm(const unsigned int dimension,const real_t mu);
real_t proxg_one_norm(const struct one_norm* data,real_t* input, real_t gamma);

#endif