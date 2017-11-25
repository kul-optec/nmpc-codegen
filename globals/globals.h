#include <math.h>
/* 
 * This file contains properties configurable by the user
 */
#ifndef GLOBALS_H
#define GLOBALS_H
    #include "globals_dyn.h"

    /* data type used to store numbers, the default type is double */
    #ifndef real_t
        #define real_t double
    #endif

    #ifndef ABS
        #define ABS(x) fabs(x)
    #endif

    /* the machine accuracy double*/
    #ifndef MACHINE_ACCURACY
        #define MACHINE_ACCURACY pow(10,-16)
    #endif

    /* large number */
    #ifndef LARGE
        #define LARGE 10000000000
    #endif

    /* return values for failure and success of function, the unix way */
    #define FAILURE 1
    #define SUCCESS 0

    /* define the 2 boolean states */
    #define TRUE 1
    #define FALSE 0


    /* 
    * ---------------------------------
    * Proximal gradient descent definitions
    * ---------------------------------
    */

    /* constant delta used to estimate lipschitz constant  */
    #ifndef PROXIMAL_GRAD_DESC_SAFETY_VALUE
        #define PROXIMAL_GRAD_DESC_SAFETY_VALUE 0.05
    #endif

    /* ---------------------------------
    * lipschitz etimator definitions
    * ---------------------------------
    */
    #ifndef DELTA_LIPSCHITZ
        #define DELTA_LIPSCHITZ pow(10,-10)
    #endif
    #ifndef DELTA_LIPSCHITZ_SAFETY_VALUE
        #define DELTA_LIPSCHITZ_SAFETY_VALUE pow(10,-6)
    #endif


    /* ---------------------------------
    * Casadi related definitions
    * ---------------------------------
    */

    /* set the casadi mem argument in function call at zero */
    #define MEM_CASADI 0 

    /* ---------------------------------
    * lbgfs solver definitions
    * ---------------------------------
    */

    #ifndef LBGFS_BUFFER_SIZE
        #define LBGFS_BUFFER_SIZE 10
    #endif

    #ifndef FBE_LINESEARCH_MAX_ITERATIONS
        #define FBE_LINESEARCH_MAX_ITERATIONS 5
    #endif

#endif