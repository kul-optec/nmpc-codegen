
#include <stdio.h>
#include <math.h>

#include "timer.h"

static struct Panoc_time time_difference;

void panoc_timer_start(void){
    printf("Not supported platform timer will give zero ! \n");
}
struct Panoc_time* panoc_timer_stop(void){

    time_difference.milli_seconds = 0;
    time_difference.micro_seconds = 0;
    time_difference.nano_seconds = 0;

    time_difference.hours = 0;
    time_difference.minutes = 0;
    time_difference.seconds = 0; 

    printf("Not supported platform timer will give zero ! \n");

    return &time_difference;
}