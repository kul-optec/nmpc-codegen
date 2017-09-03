#include<stdio.h>
#include"../../PANOC/interfaceCasadi.h"

/*
 * Simple test of the casadi interface
 * - call the function with simple input
 * - check if the output is what we expect
 */
int main(){
    printf("Starting test on casadi interface using the function in /casadi/f.c \n");
    init_func();

    real_t input_array[get_inputSize()];
    input_array[0]=1;
    input_array[1]=1;
    input_array[2]=1;
    input_array[3]=1;
    printf("GENERATING: input array with length=%d  and input=[%f,%f,%f,%f]\n", \
        get_inputSize(),input_array[0],input_array[1],input_array[2],input_array[3]);
    
    real_t output_array[get_outputSize()];
    printf("GENERATING: output array with length=%d \n",get_outputSize());

    const real_t* input = input_array;
    real_t* output = output_array;

    func(input,output);

    printf("output=[%f %f %f %f]",output[0],output[1],output[2],output[3]);
    cleanup_func();
    return FAILURE; /* return failure as the test is not ready yet */
}