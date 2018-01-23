import numpy as np
import casadi as cd
import os

def integrator_explicit_euler(x,step_size,function_system):
    x_dot = function_system(x)
    return x+step_size*x_dot

def integrator_RK(x,step_size,function_system):
    k1 = function_system(x)
    k2 = function_system(x + step_size * k1 / 2)
    k3 = function_system(x + step_size * k2 / 2)
    k4 = function_system(x + step_size * k3)
    x_new = x + (step_size / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    return  x_new

def integrator_RK_lib(x,step_size,function_system,key_name):
    """ integrate using an integration tableau from ./integrator_tableaus """
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
    # k=np.zeros((N_x,N))

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

