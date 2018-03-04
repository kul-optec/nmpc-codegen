#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>
#include"buffer.h"
#include"casadi_interface.h"

static const real_t* current_location;

static real_t current_f;
static real_t* current_df;
static real_t new_location_f;
static real_t* new_location_df;

static unsigned char precomputed_evaluations=FALSE;


int buffer_init(void){
    current_df=malloc(sizeof(real_t)*DIMENSION_PANOC);
    if(current_df==NULL) goto fail_1;

    new_location_df=malloc(sizeof(real_t)*DIMENSION_PANOC);
    if(new_location_df==NULL) goto fail_2;
    
    return SUCCESS;

    fail_2:
        free(current_df);
    fail_1:
        return FAILURE;
}
int buffer_cleanup(void){
    free(new_location_df);
    free(current_df);
    precomputed_evaluations=FALSE;
    return SUCCESS;
}
int buffer_renew(const real_t* current_location_){
    #ifdef PURE_PROX_GRADIENT
        precomputed_evaluations=FALSE;
    #endif
    current_location=current_location_;
    /*
     * only renew buffer if it wasn't precomputed
     */
    if(precomputed_evaluations==FALSE){
        current_f = casadi_interface_f_df(current_location,current_df);
    }else{
        precomputed_evaluations=FALSE;
    }
    return SUCCESS;
}
int buffer_reset_cycle(void){
    precomputed_evaluations=FALSE;
    return SUCCESS;
}

int buffer_evaluate_new_location(const real_t* lbfgs_new_location){
    new_location_f = casadi_interface_f_df(lbfgs_new_location,new_location_df);
    return SUCCESS;
}

int buffer_set_new_location_as_current_location(void){
    /*
     * Use the precomputed function/gradient evaluations as next current function/gradient values
     */
    current_f=new_location_f;

    real_t* buffer_pointer = current_df;
    current_df=new_location_df;
    new_location_df=buffer_pointer;

    /* let buffer know it should renew in next iteration */
    precomputed_evaluations=TRUE; 

    return SUCCESS;
}

/*
 * Bunch of getters on the static values, pointers are always return as pointer to const
 */
real_t buffer_get_current_f(void){return current_f;}
const real_t* buffer_get_current_location(void){return current_location;}
const real_t* buffer_get_current_df(void){return current_df;}
real_t buffer_get_new_location_f(void){return new_location_f;}
const real_t* buffer_get_new_location_df(void){return new_location_df;}