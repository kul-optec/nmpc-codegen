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

#endif