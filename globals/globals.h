#include <math.h>
#include <float.h>
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

    /* stop condition residual nmpc */
    #ifndef MIN_RESIDUAL
        #define MIN_RESIDUAL (1e-3)
    #endif

    /* minimum amount of steps Panoc always should execute */
    #ifndef PANOC_MIN_STEPS
        #define PANOC_MIN_STEPS 0
    #endif


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
        #define DELTA_LIPSCHITZ (1e-12)
    #endif
    #ifndef DELTA_LIPSCHITZ_SAFETY_VALUE
        #define DELTA_LIPSCHITZ_SAFETY_VALUE (1e-6)
    #endif


    /* ---------------------------------
    * Casadi related definitions
    * ---------------------------------
    */

    /* set the casadi mem argument in function call at zero */
    #define MEM_CASADI 0 

    #ifndef DEFAULT_OBSTACLE_WEIGHT
        #define DEFAULT_OBSTACLE_WEIGHT 1.0
    #endif

    #ifndef NUMBER_OF_OBSTACLES
        #define NUMBER_OF_OBSTACLES 0
    #endif // !NUMBER_OF_OBSTACLES
    #ifndef DEFAULT_WEIGHT_GENERAL_CONSTRAINT
        #define DEFAULT_WEIGHT_GENERAL_CONSTRAINT 1e-2 /* maybe 1? */
    #endif
    #ifndef DEFAULT_VALUE_LAMBDA
        #define DEFAULT_VALUE_LAMBDA 0 /* maybe 1? */
    #endif
    /* ---------------------------------
    * lbgfs solver definitions
    * ---------------------------------
    */

    #ifndef LBGFS_BUFFER_SIZE
        #define LBGFS_BUFFER_SIZE 50
    #endif

    #ifndef FBE_LINESEARCH_MAX_ITERATIONS
        #define FBE_LINESEARCH_MAX_ITERATIONS 10
    #endif

    #ifndef LBGFS_SAFETY_SMALL_VALUE
        #define LBGFS_SAFETY_SMALL_VALUE (10e-12)
    #endif

#endif