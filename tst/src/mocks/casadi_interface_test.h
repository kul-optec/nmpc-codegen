#ifndef CASADI_INTERFACE_TEST_H
#define CASADI_INTERFACE_TEST_H

#include "../../../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>
/* aditional init function used with mock of course */
int casadi_interface_test_init(size_t dimension_, 
    real_t (*g_)(const real_t* input),
    void (*proxg_)(real_t* state),
    real_t (*f_)(const real_t* input),
    void (*df_)(const real_t* input, real_t* output));

#endif