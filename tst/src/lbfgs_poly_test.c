#include<stdio.h>
#include<math.h>
#include"../../PANOC/lbfgs.h"
#include"../../PANOC/buffer.h"
#include"../../PANOC/matrix_operations.h"
#include"../../globals/globals.h"
#include"example_problems.h"
#include"./mocks/lbfgs_rosenbrock_interface.h"

#define DIMENSION 2
static const real_t theoretical_solution[]={0,0};
static int degree=10;
int checkIfSolutionIsReached(void);
int check2thdegreepolynomial(void);
int rosenbrock_test(void);

void print_location(const real_t* location);
void print_diff(const real_t* location,const real_t* solution);

/*
 * TEST lbfgs
 * polynomial f(x1,x2,x3) = x1^4+x2^4+ x3^4+x1^3+x2^3+ x3^3
 * f(x) =0 if x=[0 0 0 0]
 */
int main(){
    return checkIfSolutionIsReached()+ \
    check2thdegreepolynomial()+\
    rosenbrock_test(); 
}

int checkIfSolutionIsReached(void){
    printf("test1 --- \n");
    degree=10;
    size_t buffer_size =20;

    lbfgs_init(buffer_size);
    f_poly_init(DIMENSION,degree);
    buffer_init();
    lbfgs_prox_grad_descent_test_init(DIMENSION);
    
    real_t current_location[DIMENSION]={0.5,0.5};
    real_t next_location[DIMENSION]={0,0};
    real_t approx_solution[DIMENSION] ={0.017081,0.017081};

    printf("test1: starting in location x1=0.5 x2=0.5 with cost=%f\n",f_poly(current_location));

    int i;
    for ( i = 0; i < 50; i++)
    {
        buffer_renew(current_location);
        const real_t* direction = lbfgs_get_direction();
        vector_add(current_location,direction,DIMENSION,next_location);
        real_t tau =0.;
        lbfgs_update_hessian(tau,current_location,next_location);
        vector_copy(next_location,current_location,DIMENSION);
        print_location(current_location);
        /* print_diff(current_location,approx_solution); */
    }
    printf("the final cost is=%f \n",f_poly(current_location));
    lbfgs_cleanup();
    buffer_cleanup();
    lbfgs_prox_grad_descent_test_cleanup();
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

    lbfgs_init(buffer_size);
    f_poly_init(DIMENSION,degree);
    buffer_init();
    real_t current_location[DIMENSION]={0.5,0.5};
    real_t next_location[DIMENSION];
    lbfgs_prox_grad_descent_test_init(DIMENSION);

    printf("test2: starting in location x1=0.5 x2=0.5 \n");

    int i;
    for ( i = 0; i < 2; i++)
    {
        buffer_renew(current_location);
        const real_t* direction = lbfgs_get_direction();
        vector_add(current_location,direction,DIMENSION,next_location);
        real_t tau =0.;
        lbfgs_update_hessian(tau,current_location,next_location);
        vector_copy(next_location,current_location,DIMENSION);
        print_location(current_location);
    }
    
    lbfgs_cleanup();
    buffer_cleanup();
    lbfgs_prox_grad_descent_test_cleanup();

    if(current_location[0]<pow(10,-15)&&current_location[1]<pow(10,-15)){
        return SUCCESS;
        printf("end of test2:SUCCESS --- \n");
    }else{
        printf("end of test2:FAILURE --- \n");
        return FAILURE;
    }
}
real_t backtracking_linesearch(const real_t* direction,const real_t* location){
    /* do backtracking linesearch */
    real_t current_df[DIMENSION];
    df_rosenbrock(location,current_df);
    real_t gamma_armijo = 0.1;
    real_t alpha=1;

    real_t possible_location[DIMENSION];
    vector_copy(location,possible_location,DIMENSION);
    vector_add_ntimes(possible_location,direction,DIMENSION,alpha);
    while(f_rosenbrock(possible_location)>= \
            f_rosenbrock(location) + gamma_armijo * alpha * inner_product(direction,current_df,DIMENSION) ){
        alpha = alpha/2;
        if(alpha<10e-5){
            alpha=0;break;
        }
        vector_copy(location,possible_location,DIMENSION);
        vector_add_ntimes(possible_location,direction,DIMENSION,alpha);
    }
    return alpha;
}
int rosenbrock_test(void){
    degree=2;
    size_t buffer_size = 20;

    lbfgs_init(buffer_size);
    enable_rosenbrock();
    buffer_init();
    lbfgs_prox_grad_descent_test_init(DIMENSION);

    printf("test3: starting in location x1=-1.2 x2=1 optimal pint is in 1 \n");
    real_t current_location[DIMENSION]={-1.2,1.};
    real_t next_location[DIMENSION];
    real_t solution_rosen[2] = {1,1};

    int i;
    for ( i = 0; i < 10; i++)
    {
        buffer_renew(current_location);
        const real_t* direction = lbfgs_get_direction();
        vector_add(current_location,direction,DIMENSION,next_location);
        real_t tau =0.;
        lbfgs_update_hessian(tau,current_location,next_location);
        vector_copy(next_location,current_location,DIMENSION);
        printf("i=%d x1=%f x2=%f with cost=%1.16f \n",i,current_location[0],current_location[1],f_rosenbrock(current_location));
    }
    
    disable_rosenbrock();
    lbfgs_cleanup();
    buffer_cleanup();
    lbfgs_prox_grad_descent_test_cleanup();

    if(ABS(current_location[0]-1)<1e-10 && ABS(current_location[0]-1)<1e-10){
        return SUCCESS;
        printf("end of test3:SUCCESS --- \n");
    }else{
        printf("end of test3:FAILURE --- \n");
        return FAILURE;
    }
}

void print_location(const real_t* location){
    printf("x1=%f x2=%f with cost=%1.16f \n",location[0],location[1],f_poly(location));
}
void print_diff(const real_t* location,const real_t* solution){
    printf("difference -> x1=%f x2=%f with cost=%1.16f \n",ABS(location[0]-solution[0]),ABS(location[1]-solution[1]),f_poly(location));
}