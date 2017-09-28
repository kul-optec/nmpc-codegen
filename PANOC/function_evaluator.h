#ifndef FUNCTION_EVALUATOR_H
#define FUNCTION_EVALUATOR_H

#include<stddef.h>
#include"../globals/globals.h"

/*
 * This file will do all the evaluations of the functions f,df,g,proxg.
 * It will cache the evaluation of the current_location
 */

int function_evaluator_init(size_t dimension_,
    real_t (*g_)(real_t* input),
    void (*proxg_)(real_t* input, real_t* output),
    real_t (*f_)(real_t* input),
    void (*df_)(real_t* input, real_t* output));

int function_evaluator_cleanup();

/*
 * evaluate f,df,g,proxg in current_location
 */
int function_evaluator_reset_cache();

/*
 * return  f(current_location)
 */
real_t function_evaluator_get_current_f();
/*
 * return pointer to const array containing df(current_location)
 */
const real_t* function_evaluator_get_current_df();
/*
 * return g(current_location)
 */
real_t function_evaluator_get_current_g();
/*
 * return pointer to const array containing proxg(current_location)
 */
const real_t* function_evaluator_get_current_proxg();

/*
 * evaluate f(location)
 */
real_t function_evaluator_get_new_f(real_t* location);
/*
 * evaluate df_location=df(location)
 */
int function_evaluator_get_new_df(real_t* location, real_t* df_location);
/*
 * evaluate f_location=f(location) and df_location=df(location)
 */
int function_evaluator_get_new_f_df(real_t* location, real_t* f_location,real_t* df_location);
/*
 * evaluate g(location)
 */
real_t function_evaluator_get_new_g(real_t* location);
/*
 * evaluate proxg_location=proxg(location)
 */
int function_evaluator_get_new_proxg(real_t* location, real_t* proxg_location);

#endif