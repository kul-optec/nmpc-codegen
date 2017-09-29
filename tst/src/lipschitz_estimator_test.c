#include<stdio.h>
#include<math.h>
#include"../../PANOC/lipschitz.h"
#include"../../PANOC/matrix_operations.h"
#include"../../globals/globals.h"

#define DIMENSION 2
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
    real_t current_location[DIMENSION]={0.5,0.5};

    printf("Estimating lischitz on location x1=0.5 x2=0.5 \n");
    real_t lipschitz_value;
    lipschitz_value = get_lipschitz(df_grad_descent_poly_test,current_location,DIMENSION);
    

    if(abs(lipschitz_value-3.5356)<0.001){
        printf("end of test1:SUCCESS --- \n");
        return SUCCESS;
    }else{
        printf("Estimating lipschitz value %f at [0.5 0.5] while matlab simulates 3.5356 \n",lipschitz_value);
        printf("end of test1:FAILURE --- \n");
        return FAILURE;
    }  
}

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