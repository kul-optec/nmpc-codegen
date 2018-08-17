#include "../../globals/globals.h"

static void swap(real_t *x,real_t *y){
    real_t temp;
    temp = *x;
    *x = *y;
    *y = temp;
}

/*
 * Sort the array of "length" numbers ascending
 */ 
int __quicksort_ascending(real_t* numbers,unsigned int length){
    unsigned int i_left=0;
    unsigned int i_right=length-1;

    unsigned int pivot_index = length-1; /* start at the end with the pivot */
    real_t pivot = numbers[pivot_index];

    while(i_left != i_right){
            while(numbers[i_left]< pivot && (i_left < length-1))
                i_left++;
            while(numbers[i_right]>pivot && (i_right > 0 ))
                i_right--;
            if( i_left != i_right)
                swap(&numbers[i_left],&numbers[i_right]);   
    }

    if(length<3) /* if the problem was smaller then 4 then its solved */
        return SUCCESS;

    /* i_left and i_right now contain the pivot position */

    unsigned int length_left_subproblem = i_left;
    unsigned int length_right_subproblem = length-length_left_subproblem;

    __quicksort_ascending(&numbers[0],length_left_subproblem);
    __quicksort_ascending(&numbers[length_left_subproblem],length_right_subproblem);

    return SUCCESS;
}

static void swap_position(unsigned int *x,unsigned int *y){
    unsigned int temp;
    temp = *x;
    *x = *y;
    *y = temp;
}

/*
 * Sort the array of "length" numbers ascending, save the order in position array.
 * Leave the original array untouched.
 */ 
static int __quicksort_indices_ascending_with_offset(const real_t* numbers,unsigned int* position_array,const unsigned int length,const unsigned int offset){
    unsigned int i_left=0;
    unsigned int i_right=length-1;

    unsigned int pivot_index = length-1; /* start at the end with the pivot */
    real_t pivot = numbers[position_array[pivot_index+offset]];

    while(i_left != i_right){
            while(numbers[position_array[i_left+offset]]< pivot && (i_left < length-1))
                i_left++;
            while(numbers[position_array[i_right+offset]]>pivot && (i_right > 0 ))
                i_right--;
            if( i_left != i_right)
                swap_position(&position_array[i_left+offset],&position_array[i_right+offset]);   
    }

    if(length<3) /* if the problem was smaller then 4 then its solved */
        return SUCCESS;

    /* i_left and i_right now contain the pivot position */

    unsigned int length_left_subproblem = i_left;
    unsigned int length_right_subproblem = length-length_left_subproblem;

    __quicksort_indices_ascending_with_offset(numbers,position_array,length_left_subproblem,offset+0.);
    __quicksort_indices_ascending_with_offset(numbers,position_array,length_right_subproblem,offset+length_left_subproblem);

    return SUCCESS;
}

/*
 * Sort the array of "length" numbers ascending, save the order in position array.
 * Leave the original array untouched.
 */ 
int __quicksort_indices_ascending(const real_t* numbers,unsigned int* position_array,const unsigned int length){
    unsigned int i;
    for(i = 0; i < 6; i++)
        position_array[i]=i;

    unsigned int offset=0;
    return __quicksort_indices_ascending_with_offset(numbers,position_array,length, offset);
}