# a simple test of the chain dynamics:
#  if the input is held at zero the chain should come to a resting position

from chainDynCasadi import *
import sys
sys.path.insert(0, '../../src_python')
from integrators import *
import model_continious as modelc

import math
import numpy as np
import matplotlib.pyplot as plt

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

input = np.zeros([2,1]) # do not change the handle

step_size=0.01
simulation_time=5
number_of_steps= math.ceil(simulation_time/step_size)

system_equations = lambda state,input: chain_dyn(state, input, model_params)
integrator="RK"
g=0 # is not used here so just put it on zero
model =modelc.Model_continious(system_equations,g,step_size,model_params.number_of_states,model_params.number_of_inputs,integrator)

current_state = model.get_next_state(initial_state,input)
print(current_state)
for i in range(1,number_of_steps):
    new_current_state =model.get_next_state(current_state,input)
    current_state=new_current_state

final_positions = np.concatenate(\
    (np.zeros((dimension,1)),np.reshape(current_state[0:dimension*(number_of_balls+1)],(number_of_balls+1,dimension)).T)\
,axis=1)

print(current_state)
print(final_positions)

plt.plot(final_positions[0,:],final_positions[1,:])
plt.show()