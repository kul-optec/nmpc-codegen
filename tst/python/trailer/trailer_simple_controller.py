import sys
sys.path.insert(0, '../../../src_python')
import nmpccodegen as nmpc
import nmpccodegen.tools as tools
import nmpccodegen.models as models
import nmpccodegen.controller as controller
import nmpccodegen.Cfunctions as cfunctions
import nmpccodegen.example_models as example_models

import ctypes
import numpy as np
import matplotlib.pyplot as plt
import math

## -- GENERATE STATIC FILES --
# start by generating the static files and folder of the controller
location="../../../test_controller_builds/trailer_simple_controller"
tools.Bootstrapper.bootstrap(location,python_interface_enabled=True)
## -----------------------------------------------------------------

# get the continious system equations
(system_equations, number_of_states, number_of_inputs, coordinates_indices) = example_models.get_trailer_model(L=0.5)

step_size = 0.1
simulation_time = 5
number_of_steps = math.ceil(simulation_time / step_size)

integrator = "RK44"
constraint_input = cfunctions.IndicatorBoxFunction([-1,-1],[1,1]) # input needs stay within these borders
model = models.Model_continious(system_equations, constraint_input, step_size, number_of_states,\
                                number_of_inputs, coordinates_indices, integrator)

Q = np.diag([1,1,1])
R = np.eye(model.number_of_inputs, model.number_of_inputs)

reference_state=np.array([2,2,0])
reference_input=np.array([0,0])
stage_cost = controller.Stage_cost_QR(model, Q, R)
# define the controller
trailer_controller = controller.Nmpc_panoc(location,model,stage_cost )
trailer_controller.horizon = number_of_steps
trailer_controller.step_size = step_size
trailer_controller.integrator_casadi = True

# generate the code
trailer_controller.generate_code()

## -- simulate controller --
# setup a simulator to test
sim = tools.Simulator(trailer_controller.location)

initial_state=np.array([0.,0.,0.])
state=initial_state
state_history = np.zeros((number_of_states,number_of_steps))

result_simulation = sim.simulate_nmpc(state,reference_state,reference_input)

for i in range(1,number_of_steps):

    print("The optimal input is: [" + str(result_simulation.optimal_input[0]) + "," + str(result_simulation.optimal_input[0]) + "]")

    state = model.get_next_state_numpy(state,result_simulation.optimal_input)
    state_history[:,i] = np.reshape(state[:],number_of_states)

print(state_history[:,0:5])

plt.figure(1)
example_models.trailer_print(state_history)
plt.xlim([0, 2.5])
plt.ylim([0, 2.5])
plt.show()