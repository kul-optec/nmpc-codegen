#include "stdio.h"
#include "./include/nmpc.h"
#include "./PANOC/casadi_interface.h"

int main(){
    printf("Debugging controller: \n");
    size_t number_of_steps=100;
    size_t print_limit=10;

    double ref_state[3]={2,0.5,0};
    double ref_input[3]={0,0};

    double state[3]={0,0,0};
    double new_state[3];
    double input[2];

    nmpc_init();
    printf("# initial state x=%f y=%f theta=%f \n \n",state[0],state[1],state[2]);

    size_t i;
    for (i = 0; i < number_of_steps; i++)
    {
        npmc_solve(state,ref_state,ref_input,input);
        if(i<print_limit)
            printf("- Optimal input Ux=%f Uy=%f \n",input[0],input[1]);

        casadi_integrate(state,input,new_state);
        size_t j;
        for (j = 0; j < 3; j++) state[j]=new_state[j];

        if(i<print_limit)
            printf("# new state x=%f y=%f theta=%f \n \n",state[0],state[1],state[2]);
    }
    printf("# Final state x=%f y=%f theta=%f \n \n",state[0],state[1],state[2]);
    nmpc_cleanup();

    return 0;/* return success */
}
