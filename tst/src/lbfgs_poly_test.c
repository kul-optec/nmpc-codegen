#include<stdio.h>
#include<math.h>
#include"../../PANOC/lbfgs.h"
#include"../../PANOC/buffer.h"
#include"../../PANOC/matrix_operations.h"
#include"../../globals/globals.h"
#include"example_problems.h"

#define DIMENSION 2
static const real_t theoretical_solution[]={0,0};
static int degree=10;
int checkIfSolutionIsReached(void);
int check2thdegreepolynomial(void);

void print_location(const real_t* location);
void print_diff(const real_t* location,const real_t* solution);

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

    lbfgs_init(buffer_size,DIMENSION);
    f_poly_init(DIMENSION,degree);
    buffer_init();
    
    real_t current_location[DIMENSION]={0.5,0.5};
    real_t approx_solution[DIMENSION] ={0.017081,0.017081};

    printf("test1: starting in location x1=0.5 x2=0.5 with cost=%f\n",f_poly(current_location));

    size_t i;
    for ( i = 0; i < 50; i++)
    {
        buffer_renew(current_location);
        const real_t* direction = lbfgs_get_direction();
        vector_add(current_location,direction,DIMENSION,current_location);
        /* print_location(current_location); */
        print_diff(current_location,approx_solution);
    }
    printf("the final cost is=%f \n",f_poly(current_location));
    lbfgs_cleanup();
    buffer_cleanup();
    if(ABS(f_poly(current_location))<pow(10,-5)){
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

    lbfgs_init(buffer_size,DIMENSION);
    f_poly_init(DIMENSION,degree);
    buffer_init();
    real_t current_location[DIMENSION]={0.5,0.5};

    printf("test2: starting in location x1=0.5 x2=0.5 \n");

    size_t i;
    for ( i = 0; i < 2; i++)
    {
        buffer_renew(current_location);
        const real_t* direction = lbfgs_get_direction();
        vector_add(current_location,direction,DIMENSION,current_location);
        print_location(current_location);
    }
    
    lbfgs_cleanup();
    buffer_cleanup();

    if(current_location[0]<pow(10,-15)&&current_location[1]<pow(10,-15)){
        return SUCCESS;
        printf("end of test2:SUCCESS --- \n");
    }else{
        printf("end of test2:FAILURE --- \n");
        return FAILURE;
    }
}

void print_location(const real_t* location){
    printf("x1=%f x2=%f with cost=%1.16f \n",location[0],location[1],f_poly(location));
}
void print_diff(const real_t* location,const real_t* solution){
    printf("difference -> x1=%f x2=%f with cost=%1.16f \n",ABS(location[0]-solution[0]),ABS(location[1]-solution[1]),f_poly(location));
}