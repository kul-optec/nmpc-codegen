import sys
sys.path.insert(0, '../../../src_python')
import nmpc_panoc as npc
import model_continious as modelc
import example_models # this contains the chain example
import stage_costs
import math

import ctypes
import simulator
import numpy as np
import matplotlib.pyplot as plt
import math
import Cfunctions.IndicatorBoxFunction as indbox
import bootstrapper as bs

# get the continious system equations
(system_equations,number_of_states,number_of_inputs,coordinates_indices) = example_models.get_trailer_model(L=0.5)

step_size = 0.01
simulation_time = 5
number_of_steps = math.ceil(simulation_time / step_size)

integrator = "RK"
constraint_input = indbox.IndicatorBoxFunction([-2,-2],[2,2]) # input needs stay within these borders
model = modelc.Model_continious(system_equations, constraint_input, step_size, number_of_states,\
                                    number_of_inputs,coordinates_indices, integrator)

# simulate if for a bit
initial_state=np.array([0.,0.,math.pi/2])
input = np.array([0.,1.])

test = model.get_next_state(initial_state,input)

state=initial_state
state_history = np.zeros((number_of_states,number_of_steps))
for i in range(1,number_of_steps):
    state = np.asarray(model.get_next_state(state,input))
    state_history[:,i] = np.reshape(state[:],number_of_states)

print(state_history[:,0:5])

plt.figure(1)
plt.subplot(211)
plt.plot(state_history[0,:],state_history[1,:])
plt.subplot(212)
plt.plot(state_history[2,:])
plt.show()