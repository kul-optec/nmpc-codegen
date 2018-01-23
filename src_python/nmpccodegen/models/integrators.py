import numpy as np
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
    integrator_tab_location = script_location+"/integrator_tableaus/"+key_name+"npz"
    print("using integrator from file "+integrator_tab_location)

    # get the 3 matrices A,b,c that are commonly used with RK schemes
    # c | A
    #   | b^T
    integrator_tab = np.load(integrator_tab_location)
    A = integrator_tab['A']
    b = integrator_tab['b']
    c = integrator_tab['c']

    # TODO use scheme

