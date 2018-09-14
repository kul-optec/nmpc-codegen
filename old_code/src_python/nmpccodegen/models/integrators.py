import numpy as np
import casadi as cd
import os

def integrator_explicit_euler(x,step_size,function_system):
    """
    Integrate with explicit Euler

    Parameters
    ---------
    x : state
    step_size
    function_system
    """
    x_dot = function_system(x)
    return x+step_size*x_dot

def integrator_RK(x,step_size,function_system):
    """
    Integrate with Runga Kutta

    Parameters
    x : state
    step_size
    function_system
    """
    k1 = function_system(x)
    k2 = function_system(x + step_size * k1 / 2)
    k3 = function_system(x + step_size * k2 / 2)
    k4 = function_system(x + step_size * k3)
    x_new = x + (step_size / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    return  x_new

def integrator_RK_lib(x,step_size,function_system,key_name):
    """ 
    Integrate using an explicit integration tableau from ./integrator_tableaus

    Parameters
    ----------
    x : current state
    step_size : discretizator step size
    function_system : continious differential equation of the system
    behavior
    key_name : name of the integrator
          BS5         Bogacki-Shampine RK5(4)8    
          BuRK65      Butcher's RK65              
          CMR6        Calvo 6(5)                  
          DP5         Dormand-Prince RK5(4)7      
          FE          Forward Euler               
          Fehlberg45  Fehlberg RK5(4)6            
          Heun33      Heun RK 33                  
          Lambert65   Lambert                     
          MTE22       Minimal Truncation Error 22 
          Merson43    Merson RK4(3)               
          Mid22       Midpoint Runge-Kutta        
          NSSP32      non-SSPRK 32                
          NSSP33      non-SSPRK 33                
          PD8         Prince-Dormand 8(7)         
          RK44        Classical RK4               
          SSP104      SSPRK(10,4)                 
          SSP22       SSPRK 22                    
          SSP22star   SSPRK22star                 
          SSP33       SSPRK 33                    
          SSP53       SSP 53                      
          SSP54       SSP 54                      
          SSP63       SSP 63                      
          SSP75       SSP 75                      
          SSP85       SSP 85                      
          SSP95       SSP 95  

    Returns
    ------
    The next state
    """
    script_location = os.path.dirname(os.path.realpath(__file__))
    integrator_tab_location = os.path.join(os.path.join(script_location,"integrator_tableaus"),key_name+".npz")

    # get the 3 matrices A,b,c that are commonly used with RK schemes
    # c | A
    #   | b^T
    integrator_tab = np.load(integrator_tab_location)
    A = integrator_tab['A']
    b = integrator_tab['b']
    c = integrator_tab['c']

    (N,M)=A.shape
    if(len(x.shape)==1):
        (N_x,) = x.shape
        x=cd.reshape(x,(N_x,1))
    else:
        (N_x,_) = x.shape

    k=cd.SX.sym('k', N_x,N)

    for i in range(0,N):
        x_local=np.zeros((N_x,1))
        for j in range(0,i):
            x_local += (A[i,j]*cd.reshape(k[:,j],(N_x,1)))
        x_local*=step_size
        x_local += x

        y=function_system(x_local)
        k[:,i] = y

    x_new=np.zeros((N_x,1))
    for i in range(0,N):
        x_new +=b[i]*cd.reshape(k[:,i],(N_x,1))
    x_new *= step_size
    x_new +=x

    return x_new

