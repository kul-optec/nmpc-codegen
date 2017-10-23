#ifndef BUFFER_H
#define BUFFER_H

#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

int buffer_init();
int buffer_cleanup();

int buffer_renew(const real_t* current_location);

real_t buffer_get_current_f();
const real_t*  buffer_get_current_df();
const real_t* buffer_get_current_location();

#endif