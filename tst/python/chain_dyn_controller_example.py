from chainDynCasadi import *
from integrators import *
import math
import numpy as np
import matplotlib.pyplot as plt

# little hack to import the local lib and not work with the one in the path
import sys
sys.path.insert(0, '../../src_python')
import nmpc_panoc as npc
import model_continious as modelc

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
initial_state = np.array([ 0.2, 0. , 0.4,0. , 0.6 , 0. , 0.8 , 0. \
                ,1. , 0., \
                0.,0., 0.,0.,0.,0.,0.,0. ])
initial_state = initial_state.reshape([18,1])

input_zero = np.zeros([2,1]) # do not change the handle

system_equations = lambda state,input: chain_dyn(state, input, model_params)
number_of_states=model_params.number_of_states
number_of_inputs=model_params.dimension

Q=np.eye(number_of_states,number_of_states)
R=np.eye(number_of_inputs,number_of_inputs)

step_size=0.01
simulation_time=5
number_of_steps= math.ceil(simulation_time/step_size)

integrator="RK"
g=0 # is not used here so just put it on zero
model = modelc.Model_continious(system_equations,g,step_size,number_of_states,number_of_inputs,integrator)

nmpc_controller = npc.Nmpc_panoc("../../",model,Q,R)
nmpc_controller.generate_code()