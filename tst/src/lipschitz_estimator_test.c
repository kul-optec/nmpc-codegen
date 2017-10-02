#include<stdio.h>
#include<math.h>
#include"../../PANOC/lipschitz.h"
#include"../../PANOC/matrix_operations.h"
#include"../../globals/globals.h"
#include"../../PANOC/buffer.h"
#include"example_problems.h"
#include"./mocks/casadi_interface_test.h"

static const real_t theoretical_solution[]={0,0};
static int degree=5;
int simple_estimate_test(void);

real_t f_grad_descent_poly_test(const real_t* x);
void df_grad_descent_poly_test(const real_t* x ,real_t* df_x);


int main(){
    return simple_estimate_test();
}

int simple_estimate_test(void){
    printf("Test1 --- \n");
    degree=5;
    real_t current_location[2]={0.5,0.5};
    static size_t dimension=2;
    real_t w=0;/* parameter used in g1, set on 0, doesnt matter here */
    example_problems_set_init_problem1(w,dimension);
    f_poly_init(dimension,degree );
    casadi_interface_test_init(dimension, 
        g_1,
        proxg_1,
        f_poly,
        df_poly);
    buffer_init();

    printf("Estimating lischitz on location x1=0.5 x2=0.5 \n");
    real_t lipschitz_value;
    buffer_renew(current_location);
    lipschitz_value = get_lipschitz(current_location);

    buffer_cleanup();
    
    if(abs(lipschitz_value-3.5356)<0.001){
        printf("end of test1:SUCCESS --- \n");
        return SUCCESS;
    }else{
        printf("Estimating lipschitz value %f at [0.5 0.5] while matlab simulates 3.5356 \n",lipschitz_value);
        printf("end of test1:FAILURE --- \n");
        return FAILURE;
    }  
}