#include<stdio.h>
#include "../../globals/globals.h"
#include<math.h>
#include"../../PANOC/casadi_interface.h"

int testSimpleValues(real_t* input_array,real_t* output_array, real_t input1,real_t input2,real_t output1,real_t output2);
    
int main(){
    printf("Starting test on casadi interface using the function in /casadi/cost_function.c \n");
    casadi_interface_init();

    real_t current_state[DIMENSION_STATE];
    casadi_set_state(current_state);

    real_t input[casadi_interface_get_dimension()];
    real_t test_cost = casadi_interface_f(input);
    printf("%f",test_cost);
    
    casadi_interface_cleanup();
    return FAILURE; 
}