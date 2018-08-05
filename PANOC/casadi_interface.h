#ifndef CASADI_INTERFACE_H
#define CASADI_INTERFACE_H

#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

typedef struct {
    int inputSize;
    int outputSize;
    int buffer_intSize;
    int buffer_realSize;
    int* buffer_int;
    real_t* buffer_real;
    int (*cost_function)(const real_t** arg, real_t** res, int* iw, real_t* w, int mem);
} CasadiFunction;

int casadi_interface_init();
int casadi_interface_cleanup();
int casadi_prepare_cost_function(const real_t* current_state);
#ifdef INTEGRATOR_CASADI
int casadi_integrate(const real_t* state,const real_t* input,real_t* new_state);
#endif
/* size_t casadi_interface_get_dimension(); */

/* constraint related functions */
real_t casadi_get_weight_constraints(int index_constraint);/* returns zero if index was out of range */
int casadi_set_weight_constraints(int index_constraint,real_t weight);/* returns failure if the index is out of range */

/* cost functions */
#ifndef SINGLE_COST_MODE
real_t casadi_interface_f(const real_t* input);
#endif

real_t casadi_interface_f_df(const real_t* input,real_t* output);
real_t casadi_interface_g(const real_t* input);
void casadi_interface_proxg(real_t* state);


/*  
 * Function only used when using lagrangian
 */
#ifdef USE_LA
int casadi_evaluate_constraints(const real_t* inputs,real_t* constraint_values);
#endif

#endif