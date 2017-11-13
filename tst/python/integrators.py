import numpy as np

def integrator_explicit_euler(x,step_size,function_system):
    x_dot = function_system(x)
    return x+step_size*x_dot