#include "casadi_interface_test.h"
#include "../../../PANOC/casadi_interface.h"

#include "../../../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

static real_t (*g)(const real_t* input);
static void (*proxg)( real_t* state);
static real_t (*f)(const real_t* input);
static void (*df)(const real_t* input, real_t* output);

static size_t dimension;

int casadi_interface_init(const real_t* current_state){return FAILURE;}
size_t casadi_interface_get_dimension(){return dimension;}

/* test init function */
int casadi_interface_test_init(size_t dimension_, 
    real_t (*g_)(const real_t* input),
    void (*proxg_)(real_t* state),
    real_t (*f_)(const real_t* input),
    void (*df_)(const real_t* input, real_t* output)){
    
    g=g_;f=f_;proxg=proxg_;df=df_;
    dimension=dimension_;
    return SUCCESS;
}

/* cost functions */
real_t casadi_interface_f(const real_t* input){
    return f(input);
}
void casadi_interface_df(const real_t* input,real_t* output){
    df(input,output);
}
real_t casadi_interface_f_df(const real_t* input,real_t* output){
    df(input,output); /* get gradient */
    return f(input); /* get function value */
}
real_t casadi_interface_g(const real_t* input){
    return g(input);
}
void casadi_interface_proxg(real_t* state){
    proxg(state);
}