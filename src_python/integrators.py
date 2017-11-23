import numpy as np

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