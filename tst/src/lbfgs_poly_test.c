#include<stdio.h>
#include<math.h>
#include"../../PANOC/lbfgs.h"
#include"../../PANOC/matrix_operations.h"
#include"../../globals/globals.h"

#define DIMENSION 2
static const real_t theoretical_solution[]={0,0};
static int degree=10;
int checkIfSolutionIsReached(void);
int check2thdegreepolynomial(void);
// void f(real_t*x,real_t fx)
int gradient(const real_t* x ,real_t* df);
void print_location(const real_t* location);

/*
 * TEST lbfgs
 * polynomial f(x1,x2,x3) = x1^4+x2^4+ x3^4+x1^3+x2^3+ x3^3
 * f(x) =0 if x=[0 0 0 0]
 */
int main(){
    return checkIfSolutionIsReached()+ \
    check2thdegreepolynomial(); 
}

int checkIfSolutionIsReached(void){
    printf("test1 --- \n");
    degree=10;
    size_t buffer_size =10;

    lbfgs_init(buffer_size,DIMENSION,gradient);
    
    real_t direction[DIMENSION];
    real_t current_location[DIMENSION]={0.5,0.5};

    printf("starting in location x1=0.5 x2=0.5 \n");

    size_t i;
    for ( i = 0; i < 100; i++)
    {
        const real_t* direction = lbfgs_get_direction(current_location);
        vector_add(current_location,direction,DIMENSION,current_location);
        print_location(current_location);
    }
    lbfgs_cleanup();
    if(current_location[0]<pow(10,-3)&&current_location[1]<pow(10,-3)){
        printf("end of test1:SUCCESS --- \n");
        return SUCCESS;
    }else{
        printf("end of test1:FAILURE --- \n");
        return FAILURE;
    }
}

int check2thdegreepolynomial(void){
    degree=2;
    size_t buffer_size =10;

    lbfgs_init(buffer_size,DIMENSION,gradient);
    real_t current_location[DIMENSION]={0.5,0.5};

    printf("starting in location x1=0.5 x2=0.5 \n");

    size_t i;
    for ( i = 0; i < 2; i++)
    {
        const real_t* direction = lbfgs_get_direction(current_location);
        vector_add(current_location,direction,DIMENSION,current_location);
        print_location(current_location);
    }
    
    lbfgs_cleanup();
    if(current_location[0]<pow(10,-15)&&current_location[1]<pow(10,-15)){
        return SUCCESS;
        printf("end of test1:SUCCESS --- \n");
    }else{
        printf("end of test1:FAILURE --- \n");
        return FAILURE;
    }
}

int gradient(const real_t* x ,real_t*df){
    df[0] = degree*pow(x[0],degree-1) ;
    df[1] = degree*pow(x[1],degree-1);
}

void print_location(const real_t* location){
    printf("x1=%f x2=%f \n",location[0],location[1]);
}