#ifndef TIMER_H
#define TIMER_H

struct Panoc_time{
    int hours;
    int minutes;
    int seconds;
    int milli_seconds;
    int micro_seconds;
    int nano_seconds;
};

void panoc_timer_start(void);
const struct Panoc_time panoc_timer_stop(void);

#endif