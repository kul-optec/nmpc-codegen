#include "../globals/globals.h"
#include "../include/one_norm.h"
#include<stdlib.h>



struct one_norm* init_one_norm(const unsigned int dimension,const real_t mu){
    struct one_norm* data = malloc(sizeof(struct one_norm));
    if(data==NULL) return NULL;

    data->dimension=dimension;
    data->mu=mu;

    return data;
}

static real_t sign_x(real_t x) { return x<0 ? -1 : x>0 ? 1 : x;}

real_t prox_one_norm(const struct one_norm* data,real_t* input, real_t gamma){
    /* prox=sign(x)*,ax{|x_i|-\lambda,0} */
    unsigned int i;
    for (i = 0; i < data->dimension; i++){
        /* TODO: implement prox */
    }
    return 0; /* TODO: return proper value for g(x_{bar}) */
}