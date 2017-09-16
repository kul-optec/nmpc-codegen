/*
 * 
 */
#include"../include/panoc.h"

/*
 * Initialize the panoc library
 * This function should allways be called before doing anything with the panoc lib
 */
int panoc_init(){

}

/*
 * cleanup the panoc library
 * This function cleans up the memory used by the panoc algorithm, 
 * use this when you don't need the lib anymore
 */
int panoc_cleanup(){

}

/*
 * Solve the actually MPC problem, return the optimal inputs
 */
int panoc_solve(real_t* current_state,real_t* optimal_inputs){
    return 1; /* TODO , return error if called*/
}

