#include<stdio.h>
#include<math.h>
#include"../../PANOC/panoc.h"
#include"../../PANOC/matrix_operations.h"
#include"../../PANOC/casadi_interface.h"
#include"../../globals/globals.h"
#include"./mocks/casadi_interface_test.h"
#include<stdlib.h>

#include "example_problems.h"

static const real_t theoretical_solution[]={0,0};
static size_t degree=5;
int checkIfSolutionIsReached(void);
int checkIfSolutionIsReached2(void);
int rosen_test(void);

void print_location_2D(const real_t* location);

/*
 * TEST proximal gradient descent
 * polynomial f(x1,x2,x3) = x1^4+x2^4+ x3^4+x1^3+x2^3+ x3^3
 * f(x) =0 if x=[0 0 0 0]
 */
int main(){
    return checkIfSolutionIsReached()+\
    checkIfSolutionIsReached2();
    /*rosen_test();*/
}

int checkIfSolutionIsReached(void){
    printf("test1 --- \n");
    size_t dimension=2;
    degree=6;
    real_t w=2;
    example_problems_set_init_problem1(w,dimension);
    f_poly_init(dimension,degree );
    casadi_interface_test_init(dimension, 
        g_1,
        proxg_1,
        f_poly,
        df_poly);

    size_t numer_of_iterations=5;
    
    real_t* current_location=malloc(dimension*sizeof(real_t));
    current_location[0]=0.5;current_location[1]=0.5;
    real_t* next_location=malloc(dimension*sizeof(real_t));

    printf("starting in location x1=0.5 x2=0.5 \n");
    panoc_init(dimension);
    
    size_t i;
    for ( i = 0; i < numer_of_iterations; i++)
    {
            panoc_get_new_location(current_location,next_location);
            /* move the next location to the current location */
            real_t* buffer=current_location;
            current_location=next_location;
            next_location=buffer;
            /* print out the location */
            print_location_2D(current_location);
    }
    real_t final_cost = f_poly(current_location);
    free(current_location);
    free(next_location);
    panoc_cleanup();

    if(final_cost<0.01){ /* theoretical value is about 0.133333 */
        printf("end of test1:SUCCESS --- \n");
        return SUCCESS;
    }else{
        printf("end of test1:FAILURE --- \n");
        return FAILURE;
    }  
}
int checkIfSolutionIsReached2(void){
    printf("test2 --- \n");
    size_t dimension=2;
    degree=6;
    real_t w=3;
    example_problems_set_init_problem1(w,dimension);
    f_poly_init(dimension,degree );
    casadi_interface_test_init(dimension, 
        g_1,
        proxg_1,
        f_poly,
        df_poly);

    size_t numer_of_iterations=10;
    
    real_t* current_location=malloc(dimension*sizeof(real_t));
    current_location[0]=1;current_location[1]=1;
    real_t* next_location=malloc(dimension*sizeof(real_t));

    printf("starting in location x1=%f x2=%f \n",current_location[0],current_location[1]);
    panoc_init(dimension);
    
    size_t i;
    for ( i = 0; i < numer_of_iterations; i++)
    {
            panoc_get_new_location(current_location,next_location);
            /* move the next location to the current location */
            real_t* buffer=current_location;
            current_location=next_location;
            next_location=buffer;
            /* print out the location */
            print_location_2D(current_location);
    }
    real_t final_cost = f_poly(current_location);
    free(current_location);
    free(next_location);
    panoc_cleanup();   

    if(final_cost<0.01){
        printf("end of test2:SUCCESS --- \n");
        return SUCCESS;
    }else{
        printf("--> error on x: x1=%f and x2=%f \n",current_location[0],current_location[1]);
        printf("end of test2:FAILURE --- \n");
        return FAILURE;
    }  
}

int rosen_test(void){
    printf("test2 --- \n");
    size_t dimension=2;
    degree=6;
    real_t w=3;
    example_problems_set_init_problem1(w,dimension);
    f_poly_init(dimension,degree );
    casadi_interface_test_init(dimension, 
        g_3,
        proxg_3,
        f_rosenbrock,
        df_rosenbrock);
    real_t u_min=-5;
    real_t u_max=5;
    example_problems_set_init_problem3(u_min,u_max);

    size_t numer_of_iterations=10;
    
    real_t* current_location=malloc(dimension*sizeof(real_t));
    current_location[0]=-1.2;
    current_location[1]=1.;
    real_t* next_location=malloc(dimension*sizeof(real_t));

    printf("starting in location x1=%f x2=%f \n",current_location[0],current_location[1]);
    panoc_init(dimension);
    
    size_t i;
    for ( i = 0; i < numer_of_iterations; i++)
    {
            panoc_get_new_location(current_location,next_location);
            /* move the next location to the current location */
            real_t* buffer=current_location;
            current_location=next_location;
            next_location=buffer;
            /* print out the location */
            print_location_2D(current_location);
    }
    real_t final_cost = f_poly(current_location);
    free(current_location);
    free(next_location);
    panoc_cleanup();   

    if(final_cost<0.01){
        printf("end of test3:SUCCESS --- \n");
        return SUCCESS;
    }else{
        printf("--> error on x: x1=%f and x2=%f \n",current_location[0],current_location[1]);
        printf("end of test3:FAILURE --- \n");
        return FAILURE;
    }  
}

void print_location_2D(const real_t* location){
    printf("x1=%f x2=%f tau=%f cost=%f \n",location[0],location[1],panoc_get_tau(),f_poly(location));
}
