#include<stdio.h>
#include<math.h>
#include"../../PANOC/proximal_gradient_descent.h"
#include"../../PANOC/matrix_operations.h"
#include"../../PANOC/buffer.h"
#include"../../globals/globals.h"
#include"example_problems.h"
#include"./mocks/casadi_interface_test.h"


static const real_t theoretical_solution[]={0,0};
static int degree=5;
static int w=2;

int checkIfSolutionIsReached(void);
int checkIfSolutionIsReached_problem2(void);
void print_location(const real_t* location);
void print_location_2D(const real_t* location);

/*
 * TEST proximal gradient descent
 * polynomial f(x1,x2,x3) = x1^4+x2^4+ x3^4+x1^3+x2^3+ x3^3
 * f(x) =0 if x=[0 0 0 0]
 */
int main(){
    return checkIfSolutionIsReached();
}

int checkIfSolutionIsReached(void){
    printf("test1 --- \n");
    const size_t dimension=2;
    degree=5;
    size_t numer_of_iterations=100;
    real_t current_location[2]={0.5,0.5};

    printf("starting in location x1=0.5 x2=0.5 \n");
    example_problems_set_init_problem1(w,dimension);
    f_poly_init(dimension,degree );
    casadi_interface_test_init(dimension, 
        g_1,
        proxg_1,
        f_poly,
        df_poly);

    buffer_init();
    proximal_gradient_descent_init();

    size_t i;
    for ( i = 0; i < numer_of_iterations; i++)
    {
        buffer_renew(current_location);
        const real_t* direction = proximal_gradient_descent_get_direction(); /* direction = old_location - new_location */
        vector_add_ntimes(current_location,direction,dimension,-1);
        print_location_2D(current_location);
    }
    proximal_gradient_descent_cleanup();
    buffer_cleanup();

    if(current_location[0]<0.14){ /* theoretical value is about 0.133333 */
        printf("end of test1:SUCCESS --- \n");
        return SUCCESS;
    }else{
        printf("end of test1:FAILURE --- \n");
        return FAILURE;
    }  
}

void print_location_2D(const real_t* location){
    printf("x1=%f x2=%f \n",location[0],location[1]);
}
void print_location(const real_t* location){
    printf("x=%f \n",location[0]);
}