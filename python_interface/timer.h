#ifndef TIMER_H
#define TIMER_H

#define SECONDS_IN_HOURS 60*60
#define SECONDS_IN_MINUTES 60

struct Panoc_time{
    int hours;
    int minutes;
    int seconds;
    int milli_seconds;
    int micro_seconds;
    int nano_seconds;
    int panoc_interations;
};

void panoc_timer_start(void);
struct Panoc_time* panoc_timer_stop(void);

#endif