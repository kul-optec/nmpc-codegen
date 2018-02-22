#include "example_problems.h"
#include "../../PANOC/matrix_operations.h"

#include "../../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

/* internal function */
real_t sign(real_t x);

/* a polynomial as f */
static size_t f_poly_dimension;
static size_t f_poly_degree;

int f_poly_init(size_t dimension,size_t degree ){
    f_poly_dimension=dimension;
    f_poly_degree = degree;
    return SUCCESS;
}

real_t f_poly(const real_t* input){
    size_t i;
    real_t output=0;
    for (i = 0; i < f_poly_dimension; i++)
    {
        size_t exponent = f_poly_degree-1;
        real_t base = input[i];

        size_t j;real_t part_output=base;
        for (j = 0; j < exponent-1; j++)
        {
             part_output = part_output * base; 
        }
        output+= part_output;
    }
    return output;
}

void df_poly(const real_t* input,real_t* output){
    size_t i;
    for (i = 0; i < f_poly_dimension; i++)
    {
        size_t exponent = f_poly_degree-1;
        real_t base = input[i];

        size_t j;output[i]=f_poly_degree*base;
        for (j = 0; j < exponent-1; j++)
        {
             output[i] = output[i] * base; 
        }
    }
}

real_t f_rosenbrock(const real_t* x){
    real_t a =1;
    real_t b=100;

    /* Matlab: f =@(x) (a-x(1))^2 + b*(x(2)-x(1))^2; */
    real_t output=sq(a-x[0]) + b*sq(x[1]-x[0]);

    return output;
}

void df_rosenbrock(const real_t* x,real_t* output){
    real_t a =1;
    real_t b=100;
    
    /* Matlab: df = @(x) [-2*(a-(b+1)*x(1)+b*x(2)); 2*b*(x(2)-x(1)) ]; */
    output[0] = -2*(a-(b+1)*x[0]+b*x[1]);
    output[1] = 2*b*(x[1]-x[0]);
}

real_t sign(real_t x){
    if(x>=0)return 1;
    else return -1;
}

/* g(x) = max{|x|-w,0} */
static real_t problem1_w=0;
static size_t problem1_dimension=0;

int example_problems_set_init_problem1(real_t w,size_t dimension){
    problem1_w=w;
    problem1_dimension=dimension;
    return SUCCESS;
}
real_t g_1(const real_t* x){
    real_t potential_x = vector_norm1(x,problem1_dimension)-problem1_w;
    if(potential_x>0)return potential_x;
    return 0;
}
void proxg_1(real_t* x){
    real_t norm_x = vector_norm1(x,problem1_dimension);
    if(norm_x<problem1_w){/* |x|<w -> sign(x)*(|x|-w)*/
        vector_copy(x,x,problem1_dimension);
    }else if (norm_x>2*problem1_w){/* |x|>2w */
        size_t i;
        for ( i = 0; i < problem1_dimension; i++)x[i]=sign(x[i])*(ABS(x[i])-problem1_w);
    }else{/* w<|x|<2w -> sign(x)*w */
        size_t i;
        for ( i = 0; i < problem1_dimension; i++)x[i]=sign(x[i])*problem1_w; 
    }
}


/* g2=Indicator{-1;0;1} */
real_t g_2(const real_t* x){
    if(*x==-1)return 0;
    if(*x==1)return 0;
    if(*x==0)return 0;
    return LARGE;
}
void proxg_2(real_t* x){
    if(*x<-0.5){
        *x= -1;
    }else if (*x>0.5){
        *x= 1;
    }else{
        *x= 0;
    }
}

static real_t problem3_u_min=0;
static real_t problem3_u_max=0;

int example_problems_set_init_problem3(real_t u_min,real_t u_max){
    problem3_u_max=u_max;
    problem3_u_min=u_min;
    return SUCCESS;
}
/* indicator{[-u_max u_min]u[u_min u_max]} */
real_t g_3(const real_t* x){
    if(*x>problem3_u_min && *x<problem3_u_max)return 0;
    if(*x<-problem3_u_min && *x>-problem3_u_max)return 0;
    return LARGE;
}
void proxg_3(real_t* x){
    if(*x>problem3_u_min && *x<problem3_u_max)*x = *x;
    if(*x<-problem3_u_min && *x>-problem3_u_max)*x = *x;
    if(*x>problem3_u_max) *x = problem3_u_max;
    if(*x<-problem3_u_max) *x = -problem3_u_max;
    if(*x>0)*x =problem3_u_min;
    else *x =-problem3_u_min;
}