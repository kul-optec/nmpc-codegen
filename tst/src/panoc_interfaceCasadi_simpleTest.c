#include<stdio.h>
#include<math.h>
#include"../../PANOC/interfaceCasadi.h"
/*
 * Simple test of the casadi interface
 * - call the function with simple input
 * - check if the output is what we expect
 */
int testSimpleValues(real_t* input_array,real_t* output_array, real_t input1,real_t input2,real_t output1,real_t output2);
    
int main(){
    printf("Starting test on casadi interface using the function in /casadi/f.c \n");
    init_func();

    real_t input_array[get_inputSize()];
    printf("GENERATING: input array with length=%d \n",get_inputSize());
    
    real_t output_array[get_outputSize()];
    printf("GENERATING: output array with length=%d \n",get_outputSize());

    int result=SUCCESS;
    /* the cosine of PI is zero, the cosine of PI/2 is 1 */
    result += testSimpleValues(input_array,output_array,M_PI,M_PI/2,0,1);
    
    cleanup_func();
    return result; 
}

/*
 * test if solution is with 3 digits of predicted
 */
int testSimpleValues(real_t* input_array,real_t* output_array,\
    real_t input1,real_t input2,real_t output1,real_t output2){

    input_array[0]=input1;
    input_array[1]=input2;
    
    const real_t* input = input_array;
    real_t* output = output_array;

    func(input,output);
    
    if(fabs(output[0]-output1)>pow(10,-3) || fabs(output[1]-output2)>pow(10,-3)){
        printf("--- TEST FAILED --- \n");
        printf("f([%f %f])=[%f %f] the predicted output was [%f %f] \n", \
            input1,input2,output[0],output[1],output1,output2);
        printf("--- END TEST --- \n");
        return FAILURE;
    }
    else 
        return SUCCESS;
}