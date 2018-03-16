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
/*
 * problem:
 *     p = x^6 + y^6
 *     norm(gradient(f)) = sqrt((6*5*x^4)^2+(6*5*y^4)^2)
 * 
 *     estimate in point [ 0.5 0.5 ]
 *     matlab solution =  norm(p(0.5+10^-10,0.5+10^-10)-p(0.5,0.5))/(sqrt(2)*10^-10) = 2.6517
 *     theoretical = sqrt((6*5*0.5^4)^2+(6*5*0.5^4)^2) = 2.6517
 */
int simple_estimate_test(void){
    printf("Test1 --- \n");
    degree=6;
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
    lipschitz_value = get_lipschitz();

    buffer_cleanup();
    
    if(ABS(lipschitz_value-2.6517)<0.001){
        printf("end of test1:SUCCESS --- \n");
        return SUCCESS;
    }else{
        printf("Estimating lipschitz value %f at [0.5 0.5] theoretical is 2.6517 \n",lipschitz_value);
        printf("end of test1:FAILURE --- \n");
        return FAILURE;
    }  
}