#include "timer.h"
#define real_t double

#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT        
#endif


/*
 * Simulates the controller and fill optimal_input with the optimal input.
 * -> returns the time till convergence
 */
EXPORT void simulation_init();
EXPORT struct Panoc_time* simulate_nmpc_panoc( real_t* current_state,
                                        real_t* optimal_inputs,
                                        real_t* state_reference,
                                        real_t* input_reference
                                        );

EXPORT int get_last_full_solution(real_t* output);
EXPORT void simulation_cleanup();

EXPORT real_t simulation_get_weight_constraints(int index_constraint);
EXPORT int simulation_set_weight_constraints(int index_constraint,real_t weight);
EXPORT int simulation_set_buffer_solution(real_t value, int index);
EXPORT real_t simulation_evaluate_f_df(real_t* static_casadi_parameters,real_t* input, real_t* output);
EXPORT real_t simulation_evaluate_f(real_t* static_casadi_parameters,real_t* input);
EXPORT real_t get_last_buffered_cost(void);