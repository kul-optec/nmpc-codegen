#include "../../globals/globals.h"

/*
 * sort the array of "length" numbers ascending
 */ 
int __quicksort_ascending(real_t* numbers,unsigned int length);

/*
 * Sort the array of "length" numbers ascending, save the order in position array.
 * Leave the original array untouched.
 */ 
int __quicksort_indices_ascending(const real_t* numbers,unsigned int* position_array,const unsigned int length);