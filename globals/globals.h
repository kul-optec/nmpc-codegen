/* 
 * This file contains properties configurable by the user
 */
#ifndef GLOBALS_H
#define GLOBALS_H

/* data type used to store numbers, the default type is double */
#define real_t double
/* the machine accuracy double*/
#define real_eps pow(10,-16)
/* return values for failure and success */
#define FAILURE 1
#define SUCCESS 0
/* define the 2 boolean states */
#define TRUE 1
#define FALSE 0


/* 
 * ---------------------------------
 * START globals proximal gradient descent
 * ---------------------------------
 */

/* constant delta used to estimate lipschitz constant  */
#define DELTA_LIPSCHITZ pow(10,-5)

#define PROXIMAL_GRAD_DESC_SAFETY_VALUE 0.05

/* ---------------------------------
 * END globals LIPSCHITZ CONSTANTS
 * ---------------------------------
 */


/* ---------------------------------
 * Casadi related definitions
 * ---------------------------------
 */

/* set the casadi mem argument in function call at zero */
#define MEM_CASADI 0 

#endif