#include "../globals/globals.h"
#include "../include/indicator_L0ball.h"
#include <stdlib.h>
#include "internal_lib/quicksort.h"

struct indicator_bin* init_L0ball(\
    const unsigned int dimension,const unsigned int number_of_non_zero_elements){

    struct L0ball* data = malloc(sizeof(struct L0ball));
    if(data==NULL) goto fail_1;

    data->positions=malloc(data->dimension*sizeof(int));
    if(data->positions==NULL) goto fail_2;

    data->dimension=dimension;
    data->number_of_non_zero_elements=number_of_non_zero_elements;

    return data;

    fail_2:
        free(data);
    fail_1:
        return NULL;
}

real_t prox_indicator_bin(const struct L0ball* data,real_t* input, real_t gamma){
    real_t g=0.*gamma; /* the new pont x is by definition allway's inside the box */

    /* 
     * Put the lowest elements on zero 
     */
    __quicksort_indices_ascending(input,data->positions,data->dimension);
    unsigned int i;
    for(i = 0; i < data->number_of_non_zero_elements; i++){
        input[data->positions[i]]=0;
    }
    
    return g;
}