#include <windows.h> 

#include <stdio.h>
#include <math.h>

#include "timer.h"

/*
 * Implementation of the Timer lib on windows using MINGW
 */
static struct Panoc_time time_difference;
static LARGE_INTEGER t1, t2;
static LARGE_INTEGER frequency; 

static void find_time_difference(void);

void panoc_timer_start(void){
    /* get ticks at start */
    QueryPerformanceCounter(&t1);
    
}
struct Panoc_time* panoc_timer_stop(void){
    /* get current ticks */
    QueryPerformanceCounter(&t2);

    find_time_difference();

    return &time_difference;
}

static void convert_time_format(long int seconds,long int remaining_ticks){
    /* convert seconds into seconds/minutes/hours */
    time_difference.hours =(int) (seconds /  SECONDS_IN_HOURS); 
    long difference_hours = (long)time_difference.hours*(long) SECONDS_IN_HOURS;

    time_difference.minutes = (int)((seconds- difference_hours)/ SECONDS_IN_MINUTES); 
    long difference_minutes = (long)time_difference.minutes*(long) SECONDS_IN_MINUTES;

    time_difference.seconds = (int)((seconds- difference_hours) - difference_hours - difference_minutes); 

    /* convert remaining ticks into milli/micro/nano seconds */
    long int ticks_per_ms = frequency.QuadPart/1000;
    long int ticks_per_us = frequency.QuadPart/1000000;
    long int ticks_per_ns = frequency.QuadPart/1000000000;

    if(remaining_ticks>0 && ticks_per_ms>0){
        time_difference.milli_seconds=remaining_ticks/ticks_per_ms;
        remaining_ticks = remaining_ticks % ticks_per_ms;
    }else
        time_difference.milli_seconds=0;

    if(remaining_ticks>0 && ticks_per_us>0){
        time_difference.micro_seconds=remaining_ticks/ticks_per_us;
        remaining_ticks = remaining_ticks % ticks_per_us;
    }else
        time_difference.micro_seconds=0;

    if(remaining_ticks>0 && ticks_per_ns>0)
        time_difference.nano_seconds=remaining_ticks/ticks_per_ns;
    else
        time_difference.nano_seconds=0;
}

static void find_time_difference(void){
    /* get ticks per second */
    QueryPerformanceFrequency(&frequency);

    long int seconds = (t2.QuadPart - t1.QuadPart) / frequency.QuadPart;
    long int remaining_ticks = (t2.QuadPart - t1.QuadPart) %  frequency.QuadPart;

    while(remaining_ticks<0){
        seconds--;
        remaining_ticks+= (long double) frequency.QuadPart;
    }

    convert_time_format(seconds,remaining_ticks);
}