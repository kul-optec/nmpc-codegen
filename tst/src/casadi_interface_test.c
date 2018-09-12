#include<stdio.h>
#include "../../globals/globals.h"
#include<math.h>
#include"../../PANOC/casadi_interface.h"
#include"../../PANOC/matrix_operations.h"

#define DIMENSION_PANOC_EXAMPLE 100

int test_casadi_interface_f(void);
int test_casadi_interface_df(void);
int simple_test_integrator(void);
int check_positions(const real_t* state,const real_t* required_state);

static int number_of_masses=4;
static real_t state_reference[DIMENSION_STATE]={0.1932, -5.9190 , 0.3874,-8.8949,0.6126,-8.8949,0.8068,-5.9190 \
                ,1. , 0., \
                0.,0., 0.,0.,0.,0.,0.,0.};
static real_t input_reference[20]={ 0,0,0,0,0,
                                    0,0,0,0,0,
                                    0,0,0,0,0,
                                    0,0,0,0,0};

static void print_success(void){
    printf("## TEST SUCCEEDED ## \n");
}

int main(){
    int test_result1 = test_casadi_interface_f();
    int test_result2 = test_casadi_interface_df();
        // simple_test_integrator();
    return test_result1+test_result2;
}

int test_casadi_prepare_static_casadi_parameters(real_t* static_casadi_parameters,\
                real_t* current_state,real_t* state_reference,real_t* input_reference){
    int i;
    for(i=0;i<DIMENSION_STATE;i++){
        static_casadi_parameters[i] = current_state[i];
        static_casadi_parameters[i+DIMENSION_STATE] = state_reference[i];
    }
    for(i=0;i<DIMENSION_INPUT;i++){
        static_casadi_parameters[i+2*DIMENSION_STATE] = input_reference[i];
    }
    return SUCCESS;
}

int test_casadi_interface_f(void){
    printf("-----------------\n");
    printf("Starting test on casadi interface using the function in /casadi/cost_function.c \n");
    casadi_interface_init();

    real_t* zero_input=calloc(sizeof(real_t),DIMENSION_PANOC_EXAMPLE);

    real_t current_state[DIMENSION_STATE]={0.1932, -5.9190 , 0.3874,-8.8949,0.6126,-8.8949,0.8068,-5.9190 \
                ,1. , 0., \
                0.,0., 0.,0.,0.,0.,0.,0.};

    real_t static_casadi_parameters[2*DIMENSION_STATE+DIMENSION_INPUT];
                
    test_casadi_prepare_static_casadi_parameters(static_casadi_parameters,current_state,state_reference,input_reference);
    casadi_prepare_cost_function(static_casadi_parameters);
    real_t test_cost_optimal = casadi_interface_f(zero_input);

    real_t lower_state[DIMENSION_STATE]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    vector_add_ntimes(lower_state,current_state,DIMENSION_STATE,0.8);
    
    test_casadi_prepare_static_casadi_parameters(static_casadi_parameters,current_state,state_reference,input_reference);
    casadi_prepare_cost_function(static_casadi_parameters);
    real_t test_cost_to_low = casadi_interface_f(zero_input);

    real_t higher_state[DIMENSION_STATE]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    vector_add_ntimes(higher_state,current_state,DIMENSION_STATE,1.5);
    
    test_casadi_prepare_static_casadi_parameters(static_casadi_parameters,current_state,state_reference,input_reference);
    casadi_prepare_cost_function(static_casadi_parameters);
    real_t test_cost_to_high = casadi_interface_f(zero_input);

    printf("test of f \n");
    printf("The 3 costs are: %f - %f - %f\n",test_cost_to_low,test_cost_optimal,test_cost_to_high); 
    if(test_cost_to_low<test_cost_optimal) {
        printf("ERROR: lower state should give higher cost! \n");
        return FAILURE;
    }
    if(test_cost_to_high<test_cost_optimal) {
        printf("ERROR: higher state should give higher cost! \n");
        return FAILURE;
    }
    
    free(zero_input);
    casadi_interface_cleanup();
    print_success();
    return SUCCESS; 
}
int test_casadi_interface_df(void){
    printf("-----------------\n");
    printf("Starting test on casadi interface using the function in /casadi/cost_function_derivative_combined.c \n");
    casadi_interface_init();

    real_t current_state[DIMENSION_STATE]={0.1932, -5.9190 , 0.3874,-8.8949,0.6126,-8.8949,0.8068,-5.9190 \
                ,1. , 0., \
                0.,0., 0.,0.,0.,0.,0.,0.};

    /* test on current state */
    real_t* zero_input=calloc(sizeof(real_t),DIMENSION_PANOC_EXAMPLE);
    real_t static_casadi_parameters[2*DIMENSION_STATE+DIMENSION_INPUT];
                      
    test_casadi_prepare_static_casadi_parameters(static_casadi_parameters,current_state,state_reference,input_reference);
    casadi_prepare_cost_function(static_casadi_parameters);
    real_t* test_cost_optimal=malloc(sizeof(real_t)*DIMENSION_PANOC_EXAMPLE);
    casadi_interface_f_df(zero_input,test_cost_optimal);
    /* --------------------- */

    /* test on lower current state */
    real_t* lower_state=calloc(sizeof(real_t),DIMENSION_STATE);
    vector_add_ntimes(lower_state,current_state,18,0.8);
    
    test_casadi_prepare_static_casadi_parameters(static_casadi_parameters,current_state,state_reference,input_reference);
    casadi_prepare_cost_function(static_casadi_parameters);
    real_t* test_cost_to_low=malloc(sizeof(real_t)*DIMENSION_PANOC_EXAMPLE);
    casadi_interface_f_df(zero_input,test_cost_to_low);

    free(lower_state);
    /* --------------------- */

    /* test on higher current state */
    real_t* higher_state=calloc(sizeof(real_t),DIMENSION_STATE);
    vector_add_ntimes(higher_state,current_state,18,1.5);
        
    test_casadi_prepare_static_casadi_parameters(static_casadi_parameters,current_state,state_reference,input_reference);
    casadi_prepare_cost_function(static_casadi_parameters);
    real_t* test_cost_to_high=malloc(sizeof(real_t)*DIMENSION_PANOC_EXAMPLE);
    casadi_interface_f_df(zero_input,test_cost_to_high);
    free(higher_state);
    /* --------------------- */

    printf("{%f %f} \n",test_cost_to_low[0],test_cost_to_low[1]);
    printf("{%f %f} \n",test_cost_optimal[0],test_cost_optimal[1]);
    printf("{%f %f} \n",test_cost_to_high[0],test_cost_to_high[1]);
    
    free(zero_input);
    free(test_cost_optimal);
    free(test_cost_to_low);free(test_cost_to_high);
    casadi_interface_cleanup();
    print_success();
    return SUCCESS; 
}

int simple_test_integrator(void){
    printf("-----------------\n");
    printf("Starting test on integrator at  \n");
    casadi_interface_init();

    real_t input[2]={0,0};
    real_t start_state[DIMENSION_STATE]={0.1932, -5.9190 , 0.3874,-8.8949,0.6126,-8.8949,0.8068,-5.9190 \
                ,1. , 0., \
                0.,0., 0.,0.,0.,0.,0.,0.};

    real_t* current_state=malloc(sizeof(real_t)*DIMENSION_STATE);
    int i;
    for (i = 0; i < DIMENSION_STATE; i++)current_state[i]=start_state[i];
    real_t* new_state=malloc(sizeof(real_t)*DIMENSION_STATE);

    int number_of_simulations=1000;
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
    if(return_value==SUCCESS) print_success();
    return return_value; 
}

int check_positions(const real_t* state,const real_t* required_state){
    int i;int return_value=SUCCESS;
    for (i = 0; i < number_of_masses; i++)
    {
        printf(" mass %d [%f , %f] ",i,state[i*2],state[i*2+1]);
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