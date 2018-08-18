#include "../globals/globals.h"
#include "../include/one_norm.h"
#include<stdlib.h>


#define SUM(arr, len, sum) do { int i; for(i = 0; i < len; ++i) sum += arr[i]; } while(0);


struct one_norm* init_one_norm(const unsigned int dimension,const real_t mu){
    struct one_norm* data = malloc(sizeof(struct one_norm));
    if(data==NULL) return NULL;

    data->dimension=dimension;
    data->mu=mu;

    return data;
}

static real_t sign_x(real_t x) { return x<0 ? -1 : x>0 ? 1 : x;}


struct L1_norm* prox_one_norm(const struct one_norm* data,real_t* input, real_t gamma){
    /* prox=sign(x)*max{|x_i|-\lambda,0} */
    unsigned int i;
    lamda    = data->mu * gamma;
    real_t g = 0.*lamda; 

    for (i = 0; i < data->dimension; i++){
        intermediate[i] = fmax(0.0, abs(input[i]) - lamda);
        prox[i]   = sign_x(input[i])*intermediate[i];
    }
    struct output { 
        prox;
        g_prox = data->mu*SUM(intermediate, data->dimension, sum);  
    }
    /* return strcut containging proximal point= x_{bar} and  for g(x_{bar}) = mu * ||x_{bar}||_{1} */
    return output;
}

