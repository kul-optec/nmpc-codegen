#include<stdio.h>
#include "../../globals/globals.h"
#include<math.h>
#include"../../PANOC/casadi_interface.h"
#include"../../PANOC/matrix_operations.h"

int test_casadi_interface_f(void);
int test_casadi_interface_df(void);

int main(){
    return test_casadi_interface_f()+\
        test_casadi_interface_df();
}

int test_casadi_interface_f(void){
    printf("-----------------\n");
    printf("Starting test on casadi interface using the function in /casadi/cost_function.c \n");
    casadi_interface_init();

    real_t zero_input[20]={0,0,0,0,0,
                      0,0,0,0,0,
                      0,0,0,0,0,
                      0,0,0,0,0};

    real_t current_state[DIMENSION_STATE]={0.1932, -5.9190 , 0.3874,-8.8949,0.6126,-8.8949,0.8068,-5.9190 \
                ,1. , 0., \
                0.,0., 0.,0.,0.,0.,0.,0.};

    casadi_set_state(current_state);
    real_t test_cost_optimal = casadi_interface_f(zero_input);

    real_t lower_state[DIMENSION_STATE]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    vector_add_ntimes(lower_state,current_state,18,0.8,lower_state);
    
    casadi_set_state(lower_state);
    real_t test_cost_to_low = casadi_interface_f(zero_input);

    real_t higher_state[DIMENSION_STATE]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    vector_add_ntimes(higher_state,current_state,18,1.5,higher_state);
    
    casadi_set_state(higher_state);
    real_t test_cost_to_high = casadi_interface_f(zero_input);

    printf("test of f");
    printf("The 3 costs are: %f - %f - %f\n",test_cost_to_low,test_cost_optimal,test_cost_to_high); 
    if(test_cost_to_low<test_cost_optimal) return FAILURE;
    if(test_cost_to_high<test_cost_optimal) return FAILURE;
    
    casadi_interface_cleanup();
    return SUCCESS; 
}
int test_casadi_interface_df(void){
    printf("-----------------\n");
    printf("Starting test on casadi interface using the function in /casadi/cost_function.c \n");
    casadi_interface_init();

    real_t current_state[DIMENSION_STATE]={0.1932, -5.9190 , 0.3874,-8.8949,0.6126,-8.8949,0.8068,-5.9190 \
                ,1. , 0., \
                0.,0., 0.,0.,0.,0.,0.,0.};

    /* test on current state */
    real_t zero_input[20]={0,0,0,0,0,
                      0,0,0,0,0,
                      0,0,0,0,0,
                      0,0,0,0,0};
                      
    casadi_set_state(current_state);
    real_t test_cost_optimal[2];
    casadi_interface_df(zero_input,test_cost_optimal);
    /* --------------------- */

    /* test on lower current state */
    real_t lower_state[DIMENSION_STATE]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    vector_add_ntimes(lower_state,current_state,18,0.8,lower_state);
    
    
    casadi_set_state(lower_state);
    real_t test_cost_to_low[2];
    casadi_interface_df(zero_input,test_cost_to_low);
    /* --------------------- */

    /* test on higher current state */
    real_t higher_state[DIMENSION_STATE]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    vector_add_ntimes(higher_state,current_state,18,1.5,higher_state);
        
    casadi_set_state(higher_state);
    real_t test_cost_to_high[2];
    casadi_interface_df(zero_input,test_cost_to_high);
    /* --------------------- */

    printf("{%f %f} \n",test_cost_to_low[0],test_cost_to_low[1]);
    printf("{%f %f} \n",test_cost_optimal[0],test_cost_optimal[1]);
    printf("{%f %f} \n",test_cost_to_high[0],test_cost_to_high[1]);
    
    
    casadi_interface_cleanup();
    return SUCCESS; 
}