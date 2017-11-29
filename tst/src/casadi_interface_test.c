#include<stdio.h>
#include "../../globals/globals.h"
#include<math.h>
#include"../../PANOC/casadi_interface.h"

int testSimpleValues(real_t* input_array,real_t* output_array, real_t input1,real_t input2,real_t output1,real_t output2);
    
int main(){
    printf("Starting test on casadi interface using the function in /casadi/cost_function.c \n");
    casadi_interface_init();

    real_t current_state[DIMENSION_STATE]={0.1932, -5.9190 , 0.3874,-8.8949,0.6126,-8.8949,0.8068,-5.9190 \
                ,1. , 0., \
                0.,0., 0.,0.,0.,0.,0.,0.};
    casadi_set_state(current_state);

    real_t input[casadi_interface_get_dimension()];
    real_t test_cost = casadi_interface_f(input);
    printf("%f",test_cost); /* this should be about 1.99961e-023 according to the matlab version */
    
    casadi_interface_cleanup();
    return FAILURE; /* TODO implement and control mechanism to see if the test_cost value is of the size expected */
}