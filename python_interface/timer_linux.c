#define _POSIX_C_SOURCE 199309L
#include <time.h>  

#include <stdio.h>
#include <math.h>

#include "timer.h"

static struct timespec ts_start,ts_end;
static struct Panoc_time time_difference;
static void find_time_difference(void);
static void convert_time_format(const long difference_nano_seconds,const long seconds);

void panoc_timer_start(void){
    /* get time at start */
    clock_gettime(CLOCK_MONOTONIC, &ts_start);
}
struct Panoc_time* panoc_timer_stop(void){
    /* get current time */
    clock_gettime(CLOCK_MONOTONIC, &ts_end);  

    find_time_difference();

    return &time_difference;
}

static void convert_time_format(const long difference_nano_seconds,const long seconds){
    /* convert nanoseconds into mili/micro/nano seconds */
    time_difference.milli_seconds = (int)(difference_nano_seconds / (long) pow(10,6)); 
    long difference_milli_seconds = (long)time_difference.milli_seconds*(long) pow(10,6);

    time_difference.micro_seconds = (int)((difference_nano_seconds- difference_milli_seconds) / (long) pow(10,3)); 
    long difference_micro_seconds = (long)time_difference.micro_seconds*(long) pow(10,3);

    time_difference.nano_seconds = (int)(difference_nano_seconds- difference_milli_seconds - difference_micro_seconds);

    /* convert seconds into seconds/minutes/hours */
    time_difference.hours = (int)(seconds / (long) SECONDS_IN_HOURS); 
    long difference_hours = (long)time_difference.hours*(long) SECONDS_IN_HOURS;

    time_difference.minutes = (int)((seconds- difference_hours)/ (long) SECONDS_IN_MINUTES); 
    long difference_minutes = (long)time_difference.minutes*(long) SECONDS_IN_MINUTES;

    time_difference.seconds = (int)((seconds- difference_hours) - difference_hours - difference_minutes); 
}

static void find_time_difference(void){
    long difference_nano_seconds = ts_end.tv_nsec - ts_start.tv_nsec;

    /* make sure the nano seconds are positive */
    long seconds = 0;
    if(difference_nano_seconds<0){
        difference_nano_seconds += pow(10,9);
        seconds+=-1;
    }
    seconds=seconds+(long)(ts_end.tv_sec - ts_start.tv_sec);

    convert_time_format(difference_nano_seconds, seconds);
}