from chainDynCasadi import *
from integrators import *
import math
import numpy as np
import matplotlib.pyplot as plt

# little hack to import the local lib and not work with the one in the path
import sys
sys.path.insert(0, '../../src_python')
import nmpc_panoc as npc

# model parameters(use the same as the Matlab code):
dimension=2
number_of_balls=4 # M
ball_mass=0.03 # m
spring_constant=0.1 # D
rest_length_of_springs=0.033 # L
gravity_acceleration=9.81

model_params = Chain_dyn_parameters(dimension,number_of_balls,ball_mass,
spring_constant,rest_length_of_springs,gravity_acceleration)

# initial state:
x0 = np.array([ 0.2, 0. , 0.4,0. , 0.6 , 0. , 0.8 , 0. \
                ,1. , 0., \
                0.,0., 0.,0.,0.,0.,0.,0. ])
x0 = x0.reshape([18,1])

u = np.zeros([2,1]) # do not change the handle

function_system = lambda x: chainDynCasadi.chain_dyn(x, u, model_params)

f=function_system
g=0 # TODO
d=lambda x,steps:  0*x*steps
x_dimension=model_params.number_of_states
u_dimension=model_params.number_of_inputs

nmpc_controller = npc.Nmpc_panoc("../../",f,g,d,x_dimension,u_dimension)
nmpc_controller.generate_code("./test.c")
