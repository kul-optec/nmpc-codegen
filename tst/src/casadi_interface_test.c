#include<stdio.h>
#include "../../globals/globals.h"
#include<math.h>
#include"../../PANOC/casadi_interface.h"
#include"../../PANOC/matrix_operations.h"

int test_casadi_interface_f(void);
int test_casadi_interface_df(void);
int simple_test_integrator(void);
int check_positions(const real_t* state,const real_t* required_state);

static size_t number_of_masses=4;

int main(){
    return test_casadi_interface_f()+\
        test_casadi_interface_df()+\
        simple_test_integrator();
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
    casadi_interface_f_df(zero_input,test_cost_optimal);
    /* --------------------- */

    /* test on lower current state */
    real_t lower_state[DIMENSION_STATE]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    vector_add_ntimes(lower_state,current_state,18,0.8,lower_state);
    
    
    casadi_set_state(lower_state);
    real_t test_cost_to_low[2];
    casadi_interface_f_df(zero_input,test_cost_to_low);
    /* --------------------- */

    /* test on higher current state */
    real_t higher_state[DIMENSION_STATE]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    vector_add_ntimes(higher_state,current_state,18,1.5,higher_state);
        
    casadi_set_state(higher_state);
    real_t test_cost_to_high[2];
    casadi_interface_f_df(zero_input,test_cost_to_high);
    /* --------------------- */

    printf("{%f %f} \n",test_cost_to_low[0],test_cost_to_low[1]);
    printf("{%f %f} \n",test_cost_optimal[0],test_cost_optimal[1]);
    printf("{%f %f} \n",test_cost_to_high[0],test_cost_to_high[1]);
    
    
    casadi_interface_cleanup();
    return SUCCESS; 
}

int simple_test_integrator(void){
    printf("-----------------\n");
    printf("Starting test on npmc at  \n");
    casadi_interface_init();

    real_t input[2]={0,0};
    real_t start_state[DIMENSION_STATE]={0.1932, -5.9190 , 0.3874,-8.8949,0.6126,-8.8949,0.8068,-5.9190 \
                ,1. , 0., \
                0.,0., 0.,0.,0.,0.,0.,0.};

    real_t* current_state=malloc(sizeof(real_t)*DIMENSION_STATE);
    size_t i;
    for (size_t i = 0; i < DIMENSION_STATE; i++)current_state[i]=start_state[i];
    real_t* new_state=malloc(sizeof(real_t)*DIMENSION_STATE);

    size_t number_of_simulations=1000;
    for ( i = 0; i < number_of_simulations; i++)
    {
        casadi_integrate(current_state,input,new_state);

        real_t* buffer=current_state;
        current_state=new_state;
        new_state=buffer;

        
    }
    int return_value = check_positions(current_state,start_state);

    free(current_state);
    free(new_state);
    casadi_interface_cleanup();
    return return_value; 
}

int check_positions(const real_t* state,const real_t* required_state){
    int i;int return_value=SUCCESS;
    for (i = 0; i < number_of_masses; i++)
    {
        printf(" mass%d [%f , %f] ",i,state[i*2],state[i*2+1]);
        real_t sensitivity = 0.1;
        real_t difference_1 = ABS(state[i*2]-required_state[i*2]);
        real_t difference_2 = ABS(state[i*2+1]-required_state[i*2+1]);
        if(difference_1>sensitivity || difference_2>sensitivity){
            printf("\n ERROR difference is %f and %f \n",difference_1,difference_2);
            return_value=FAILURE;
        }
    }
    printf("\n");
    return return_value;
}