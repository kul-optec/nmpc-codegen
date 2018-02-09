#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>
#include"buffer.h"
#include"casadi_interface.h"

static real_t current_f;
static real_t* current_df;
static const real_t* current_location;

int buffer_init(void){
    current_df=malloc(sizeof(real_t)*casadi_interface_get_dimension());
    if(current_df==NULL) goto fail_1;
    
    return SUCCESS;

    fail_1:
        return FAILURE;
}
int buffer_cleanup(void){
    free(current_df);
    return SUCCESS;
}
int buffer_renew(const real_t* current_location_){
    current_location=current_location_;
    current_f = casadi_interface_f_df(current_location,current_df);
    return SUCCESS;
}

real_t buffer_get_current_f(void){return current_f;}
const real_t* buffer_get_current_location(void){return current_location;}
const real_t*  buffer_get_current_df(void){return current_df;}
