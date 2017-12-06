#include<stdio.h>
#include "../../globals/globals.h"
#include<math.h>
#include"../../PANOC/casadi_interface.h"
#include"../../PANOC/matrix_operations.h"
#include"../../include/nmpc.h"

static size_t number_of_masses=4;

int check_positions(const real_t* state,const real_t* required_state);
int simple_test(void);
int simple_test_steady_state(void);
int print_input(real_t* input);

int main(){
    return simple_test_steady_state()+\
        simple_test();
    return SUCCESS;
}

int simple_test_steady_state(void){
    printf("-----------------\n");
    printf("Starting Test1 on npmc at  \n");
    nmpc_init();

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
        /* find input trough the nmpc problem */
        npmc_solve(current_state,input);
        printf("iteration %d: ",(int)i);
        print_input(input);

        /* integrate the system to apply the input */
        casadi_integrate(current_state,input,new_state);

        /* set the new state as the next state */
        real_t* buffer=current_state;
        current_state=new_state;
        new_state=buffer;        
    }
    int return_value = check_positions(current_state,start_state);

    free(current_state);
    free(new_state);
    nmpc_cleanup();
    return return_value; 
}

int simple_test(void){
    printf("-----------------\n");
    printf("Starting Test2 on npmc at  \n");
    nmpc_init();

    real_t input[2]={0,0};
    real_t start_state[DIMENSION_STATE]={0.2, 0, 0.4, 0, 0.6, 0, 0.8, 0 \
                ,1. , 0., \
                0.,0., 0.,0.,0.,0.,0.,0.};
    real_t rest_state[DIMENSION_STATE]={0.1932, -5.9190 , 0.3874,-8.8949,0.6126,-8.8949,0.8068,-5.9190 \
                ,1. , 0., \
                0.,0., 0.,0.,0.,0.,0.,0.};

    real_t* current_state=malloc(sizeof(real_t)*DIMENSION_STATE);
    size_t i;
    for (size_t i = 0; i < DIMENSION_STATE; i++)current_state[i]=start_state[i];
    real_t* new_state=malloc(sizeof(real_t)*DIMENSION_STATE);

    size_t number_of_simulations=100;
    for ( i = 0; i < number_of_simulations; i++)
    {
        /* find input trough the nmpc problem */
        npmc_solve(current_state,input);
        printf("iteration %d: ",(int)i);
        print_input(input);

        /* integrate the system to apply the input */
        casadi_integrate(current_state,input,new_state);

        /* set the new state as the next state */
        real_t* buffer=current_state;
        current_state=new_state;
        new_state=buffer;        
    }
    int return_value = check_positions(current_state,rest_state);

    free(current_state);
    free(new_state);
    nmpc_cleanup();
    return return_value; 
}

int print_input(real_t* input){
    printf("Applying input [%f,%f] \n",input[0],input[1]);
    return SUCCESS;
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