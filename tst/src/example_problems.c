#include "example_problems.h"
#include "../../PANOC/matrix_operations.h"

#include "../../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

/* internal function */
real_t sign(real_t x);

/* a polynomial as f */
static size_t f_poly_dimension;
static int f_poly_degree;

int f_poly_init(size_t dimension,int degree ){
    f_poly_dimension=dimension;
    f_poly_degree = degree;
    return SUCCESS;
}

real_t f_poly(const real_t* input){
    size_t i;
    real_t output=0;
    for (i = 0; i < f_poly_dimension; i++)
    {
        output+= pow(input[i],f_poly_degree);
    }
    return output;
}

void df_poly(const real_t* input,real_t* output){
    size_t i;
    for (i = 0; i < f_poly_dimension; i++)
    {
        output[i]= f_poly_degree*pow(input[i],f_poly_degree-1);
    }
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
void proxg_1(const real_t* x ,real_t* proxg_x){
    real_t norm_x = vector_norm1(x,problem1_dimension);
    if(norm_x<problem1_w){/* |x|<w -> sign(x)*(|x|-w)*/
        vector_copy(x,proxg_x,problem1_dimension);
    }else if (norm_x>2*problem1_w){/* |x|>2w */
        size_t i;
        for ( i = 0; i < problem1_dimension; i++)proxg_x[i]=sign(x[i])*(ABS(x[i])-problem1_w);
    }else{/* w<|x|<2w -> sign(x)*w */
        size_t i;
        for ( i = 0; i < problem1_dimension; i++)proxg_x[i]=sign(x[i])*problem1_w; 
    }
}