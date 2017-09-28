#include "../globals/globals.h"
#include <stddef.h>
#include <stdlib.h>

#define OUT_OF_DATE 0
#define UP_TO_DATE 1

real_t (*g)(real_t* input);
void (*proxg)(real_t* input, real_t* output);
real_t (*f)(real_t* input);
void (*df)(real_t* input,real_t* output);

size_t dimension;

/* 
 * the cache:
 */
static struct cache_function_evaluations{
real_t f;
real_t* df;
real_t g;
real_t* proxg;
}cache;
/*
 * STATUS of the internet cache, should we reevaluate the function or not?
 */
static struct function_evaluation_state{
int f_df;
int g;
int proxg;
} state;

/*
 * call this function at the start of your program
 */
int function_evaluator_init(size_t dimension_,
    real_t (*g_)(real_t* input),
    void (*proxg_)(real_t* input, real_t* output),
    real_t (*f_)(real_t* input),
    void (*df_)(real_t* input, real_t* output)){
        dimension=dimension_;
        f=f_;df=df_;g=g_;proxg=proxg_;

    state.f_df=OUT_OF_DATE;
    state.g=OUT_OF_DATE;
    state.proxg=OUT_OF_DATE;

    cache.df=malloc(sizeof(real_t)*dimension);
    if(cache.df==NULL)goto fail_1;

    cache.proxg=malloc(sizeof(real_t)*dimension);
    if(cache.proxg==NULL)goto fail_2;

    return SUCCESS;

    fail_2:
        free(cache.df);
    fail_1:
        return FAILURE;
}

/*
 * cleans up all the variables
 */
int function_evaluator_cleanup(){
    free(cache.df);
    free(cache.proxg);
    return SUCCESS;
}

/*
 * reset the cache
 */
int function_evaluator_reset_cache(){
    state.f_df=OUT_OF_DATE;
    state.g=OUT_OF_DATE;
    state.proxg=OUT_OF_DATE;
}
/*
 * return  f(current_location)
 */
real_t function_evaluator_get_current_f(real_t* current_location){
    if(state.f_df==OUT_OF_DATE) { /* do i need to re-evaluate the function? */
        cache.f=f(current_location);
        df(current_location,cache.df);
        state.f_df=UP_TO_DATE;
    } 
    return cache.f;
}
/*
 * return pointer to const array containing df(current_location)
 */
const real_t* function_evaluator_get_current_df(real_t* current_location){
    if(state.f_df==OUT_OF_DATE) { /* do i need to re-evaluate the function? */
        cache.f=f(current_location);
        df(current_location,cache.df);
        state.f_df=UP_TO_DATE;
    } 
    return cache.df;
}
/*
 * return pointer to const array containing g(current_location)
 */
real_t function_evaluator_get_current_g(real_t* current_location){
    if(state.g==OUT_OF_DATE) { /* do i need to re-evaluate the function? */
        cache.g=f(current_location);
        state.g=UP_TO_DATE;
    } 
    return cache.g;
}
/*
 * return pointer to const array containing proxg(current_location)
 */
const real_t* function_evaluator_get_current_proxg(real_t* current_location){
    if(state.proxg==OUT_OF_DATE) {  /* do i need to re-evaluate the function? */
        proxg(current_location,cache.proxg);
        state.proxg=UP_TO_DATE;
    } 
    return cache.proxg;
}

/*
 * evaluate f_location=f(location)
 */
real_t function_evaluator_get_new_f(real_t* location){
    return f(location);
}
/*
 * evaluate df_location=df(location)
 */
int function_evaluator_get_new_df(real_t* location, real_t* df_location){
    df(location,df_location);
    return SUCCESS;
}
/*
 * evaluate f_location=f(location) and df_location=df(location)
 */
int function_evaluator_get_new_f_df(real_t* location, real_t* f_location,real_t* df_location){
    *f_location=f(location);
    df(location,df_location);
    return SUCCESS;
}
/*
 * evaluate g_location=g(location)
 */
real_t function_evaluator_get_new_g(real_t* location){
    return g(location);
}
/*
 * evaluate proxg_location=proxg(location)
 */
int function_evaluator_get_new_proxg(real_t* location, real_t* proxg_location){
    proxg(location,proxg_location);
}