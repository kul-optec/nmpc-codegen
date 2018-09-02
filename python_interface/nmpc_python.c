#include "stdlib.h"
#include "../include/nmpc.h"
#include "../PANOC/casadi_interface.h"
#include "../PANOC/buffer.h"
#include "../globals/globals.h"
#include "timer.h"
#include <stdio.h>

#include"nmpc_python.h"

static struct Panoc_time* time_difference;

/*
 * Simulates the controller and fill optimal_input with the optimal input.
 * -> returns the time till convergence
 */
void simulation_init(){
    nmpc_init();
}
struct Panoc_time* simulate_nmpc_panoc( real_t* current_state,
                                        real_t* optimal_inputs,
                                        real_t* state_reference,
                                        real_t* input_reference
                                        ){
    panoc_timer_start();

    int number_of_interations = npmc_solve(current_state,optimal_inputs,state_reference,input_reference);

    time_difference = panoc_timer_stop();

    time_difference->panoc_interations=number_of_interations;

    return time_difference;
}
int get_last_full_solution(real_t* output){
    return nmpc_get_last_full_solution(output);
}
void simulation_cleanup(){
    nmpc_cleanup();
}

real_t simulation_get_weight_constraints(int index_constraint){
    return nmpc_get_weight_constraints(index_constraint);
}
int simulation_set_weight_constraints(int index_constraint,real_t weight){
    return nmpc_set_weight_constraints(index_constraint,weight);
}
int simulation_set_buffer_solution(real_t value, int index){
    return nmpc_set_buffer_solution(value,index);
}
real_t simulation_evaluate_f_df(real_t* static_casadi_parameters,real_t* input, real_t* output){
    casadi_prepare_cost_function(static_casadi_parameters);
    return casadi_interface_f_df(input,output);
}
real_t simulation_evaluate_f(real_t* static_casadi_parameters,real_t* input){
    casadi_prepare_cost_function(static_casadi_parameters);
    #ifndef SINGLE_COST_MODE
        return casadi_interface_f(input);
    #else
        return casadi_interface_f_df(input,NULL);
    #endif
    
}
real_t get_last_buffered_cost(void){
    return buffer_get_current_f();
}