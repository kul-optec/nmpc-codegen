#include<stdio.h>
#include<math.h>
#include"../../PANOC/proximal_gradient_descent.h"
#include"../../PANOC/matrix_operations.h"
#include"../../globals/globals.h"
#include"example_problems.h"

#define DIMENSION 2
static const real_t theoretical_solution[]={0,0};
static int degree=5;
static int w=2;

int checkIfSolutionIsReached(void);
void print_location(real_t* location);

/*
 * Function f with its gradient df  
 * Function g with the resulting function after proximal operator
 */
real_t f_grad_descent_poly_test(const real_t* x);
real_t g_grad_descent_poly_test(const real_t* x);
void df_grad_descent_poly_test(const real_t* x ,real_t* df_x);
void proxg_grad_descent_poly_test(const real_t* x ,real_t* proxg_x);

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
    degree=5;
    size_t numer_of_iterations=100;
    real_t current_location[DIMENSION]={0.5,0.5};

    printf("starting in location x1=0.5 x2=0.5 \n");
    example_problems_set_init_problem1(w,DIMENSION);
    proximal_gradient_descent_init(DIMENSION, \
        g_1,\
        proxg_1,\
        f_grad_descent_poly_test,\
        df_grad_descent_poly_test);
    
    size_t i;
    for ( i = 0; i < numer_of_iterations; i++)
    {
        const real_t* direction = proximal_gradient_descent_get_direction(current_location);
        vector_add_ntimes(current_location,direction,DIMENSION,1,current_location);
        print_location(current_location);
    }
    proximal_gradient_descent_cleanup();

    if(current_location[0]<0.14){ /* theoretical value is about 0.133333 */
        printf("end of test1:SUCCESS --- \n");
        return SUCCESS;
    }else{
        printf("end of test1:FAILURE --- \n");
        return FAILURE;
    }  
}

/*
 * simple problem to test the proximal gradient descent
 */
real_t f_grad_descent_poly_test(const real_t* x){
    real_t f_x=0;
    size_t i;
    for (i = 0; i < DIMENSION; i++){
        f_x+=pow(x[i],degree);
    }
    return f_x;
}
void df_grad_descent_poly_test(const real_t* x ,real_t* df_x){
    size_t i;
    for (i = 0; i < DIMENSION; i++){
        df_x[i] = degree*pow(x[i],degree-1) ;
    }
}
void print_location(real_t* location){
    printf("x1=%f x2=%f \n",location[0],location[1]);
}