#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>
#include"buffer.h"
#include"casadi_interface.h"

static real_t current_f;
static real_t* current_df;
static const real_t* current_location;

int buffer_init(){
    current_df=malloc(sizeof(real_t)*casadi_interface_get_dimension());
    if(current_df==NULL) goto fail_1;
    
    return SUCCESS;

    fail_1:
        return FAILURE;
}
int buffer_cleanup(){
    free(current_df);
    return SUCCESS;
}

int buffer_renew(const real_t* current_location_){
    current_location=current_location_;
    current_f = casadi_interface_f_df(current_location,current_df);
    return SUCCESS;
}

real_t buffer_get_current_f(){return current_f;}
const real_t* buffer_get_current_location(){return current_location;}
const real_t*  buffer_get_current_df(){return current_df;}
