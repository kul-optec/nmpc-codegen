#include "stdlib.h"
#include "../include/nmpc.h"
#include "../globals/globals.h"

void simulation_init();
void simulation_cleanup();
real_t simulate_nmpc_panoc(real_t* current_state,real_t* optimal_inputs);
/*
 * Simulates the controller and fill optimal_input with the optimal input.
 * It returns the time till convergence
 */
void simulation_init(){
    nmpc_init();
}
real_t simulate_nmpc_panoc(real_t* current_state,real_t* optimal_inputs){
    // nmpc_init();
    real_t convergence_time=0;

    /* start timer here TODO */

    npmc_solve(current_state,optimal_inputs);

    /* stop timer here TODO */

    return convergence_time;
}
void simulation_cleanup(){
    nmpc_cleanup();
}