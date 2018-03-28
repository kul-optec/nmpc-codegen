#include "./timer.h"
#include "stdio.h"
#include "stdlib.h"
#include "math.h"
#include "time.h"

#define NUMBER_OF_CALCS 100000000
/*
 * compile Linux: gcc -std=c89 python_interface/timer_linux.c python_interface/test_timer.c  -lm  -g
 * compile windows MINGW: gcc -std=c89 .\python_interface\timer_windows.c python_interface/test_timer.c  -lm  -g
 */
static void print_time(const struct Panoc_time* time_difference);
int main(void){
    printf("START TESTING TIMER \n");
    panoc_timer_start();
    size_t i;
    double buffer=0;
    /* do some calcs to waste some time */
    for ( i = 0; i < NUMBER_OF_CALCS; i++)
    {
        buffer += sqrt(rand());
    }
    struct Panoc_time* time_difference = panoc_timer_stop();
    print_time(time_difference);
    return 0;
}

static void print_time(const struct Panoc_time* time_difference){
    printf("time executed= [%d:%d:%d  %d:%d:%d] \n",\
        time_difference->hours,time_difference->minutes,time_difference->seconds,\
        time_difference->milli_seconds,time_difference->micro_seconds,time_difference->nano_seconds);
}
