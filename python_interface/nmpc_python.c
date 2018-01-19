#include "stdlib.h"
#include "../include/nmpc.h"
#include "../globals/globals.h"
#include "timer.h"
#include <stdio.h>

void simulation_init();
void simulation_cleanup();
static struct Panoc_time* time_difference;
struct Panoc_time* simulate_nmpc_panoc(real_t* current_state,real_t* optimal_inputs);
/*
 * Simulates the controller and fill optimal_input with the optimal input.
 * -> returns the time till convergence
 */
void simulation_init(){
    nmpc_init();
}
struct Panoc_time* simulate_nmpc_panoc(real_t* current_state,real_t* optimal_inputs){
    panoc_timer_start();

    int number_of_interations = npmc_solve(current_state,optimal_inputs);

    time_difference = panoc_timer_stop();

    time_difference->panoc_interations=number_of_interations;

    return time_difference;
}
void simulation_cleanup(){
    nmpc_cleanup();
}