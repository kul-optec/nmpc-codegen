#ifndef BUFFER_H
#define BUFFER_H

#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

int buffer_init(void);
int buffer_cleanup(void);

int buffer_renew(const real_t* current_location);

real_t buffer_get_current_f(void);
const real_t*  buffer_get_current_df(void);
const real_t* buffer_get_current_location(void);

/*
 * 4 extra functions, these reuse df(x) and f(x) if it was a pure lbfgs step
 */
int buffer_evaluate_lbfgs_new_location(const real_t* lbfgs_new_location);
real_t buffer_get_lbfgs_new_location_f(void);
const real_t* buffer_get_lbfgs_new_location_df(void);
int buffer_set_lbfgs_as_precomputed(void);
#endif