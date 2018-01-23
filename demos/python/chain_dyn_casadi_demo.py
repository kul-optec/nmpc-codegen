# a simple test of the chain dynamics:
#  if the input is held at zero the chain should come to a resting position

import sys
sys.path.insert(0, '../../src_python')
import nmpccodegen as nmpc
import nmpccodegen.models as models
import nmpccodegen.example_models as example_models

import math
import numpy as np
import matplotlib.pyplot as plt

# initial state:
initial_state = np.array([ 0.2, 0. , 0.4,0. , 0.6 , 0. , 0.8 , 0. \
                ,1. , 0., \
                0.,0., 0.,0.,0.,0.,0.,0. ])
initial_state = initial_state.reshape([18,1])
input = np.zeros([2,1]) # do not change the handle

step_size=0.01
simulation_time=5
number_of_steps= math.ceil(simulation_time/step_size)

# get the continuous system equations from the existing library
(system_equations, number_of_states, number_of_inputs, coordinates_indices) = nmpc.get_chain_model()
dimension=2
number_of_balls = 4

integrator="RK44"
g=0 # is not used here so just put it on zero
model =models.Model_continious(system_equations,g,step_size,number_of_states,number_of_inputs,coordinates_indices,integrator)

current_state = model.get_next_state(initial_state,input)
for i in range(1,number_of_steps):
    new_current_state =model.get_next_state_numpy(current_state,input)
    current_state=new_current_state

final_positions = np.concatenate(\
    (np.zeros((dimension,1)),np.reshape(current_state[0:dimension*(number_of_balls+1)],(number_of_balls+1,dimension)).T)\
,axis=1)

print(final_positions)

plt.figure(1)
plt.plot(final_positions[0,:],final_positions[1,:])
plt.show()