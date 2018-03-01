import sys
sys.path.insert(0, './src_python')
import nmpccodegen as nmpc
import nmpccodegen.tools as tools
import nmpccodegen.models as models
import nmpccodegen.controller as controller
import nmpccodegen.controller.obstacles as obstacles
import nmpccodegen.Cfunctions as cfunctions
import nmpccodegen.example_models as example_models

import math
import ctypes
import numpy as np
import matplotlib.pyplot as plt

import math
import sys
import time

## -- GENERATE STATIC FILES --
# start by generating the static files and folder of the controller
trailer_controller_location = "./test_controller_builds/tutorial_controller_multishot"
tools.Bootstrapper.bootstrap(trailer_controller_location, simulation_tools=True)
## -----------------------------------------------------------------

# get the continuous system equations from the existing library
(system_equations, number_of_states, number_of_inputs, coordinates_indices) = nmpc.example_models.get_trailer_model(
    L=0.5)

step_size = 0.05
simulation_time = 10
number_of_steps = math.ceil(simulation_time / step_size)
horizon = 40

integrator = "RK44" # select a Runga-Kutta  integrator (FE is forward euler)
constraint_input = cfunctions.IndicatorBoxFunction([-1, -1], [1, 1])  # input needs stay within these borders
model = models.Model_continious(system_equations, constraint_input, step_size, number_of_states, \
                                number_of_inputs, coordinates_indices, integrator)

# Q and R matrixes determined by the control engineer.
Q = np.diag([10., 100., 1.])
R = np.eye(model.number_of_inputs, model.number_of_inputs) * 0.01

# the stage cost is defined two lines,different kinds of stage costs are available to the user.
stage_cost = controller.Stage_cost_QR(model, Q, R)

# define the controller
trailer_controller = controller.Nmpc_panoc(trailer_controller_location, model, stage_cost)
trailer_controller.horizon = horizon # NMPC parameter
trailer_controller.integrator_casadi = True # optional  feature that can generate the integrating used  in the cost function
trailer_controller.panoc_max_steps = 10000 # the maximum amount of iterations the PANOC algorithm is allowed to do.
trailer_controller.min_residual=-3
trailer_controller.shooting_mode="multiple shot"

# add an obstacle, a two dimensional rectangle
# obstacle_weight = 1000.
# rectangle = obstacles.Obstacle_rectangular(np.array([0.75,0.3]),0.5,0.2)
# trailer_controller.add_obstacle(rectangle)

# generate the dynamic code
trailer_controller.generate_code()

# -- simulate controller --
# sim.set_weight_obstacle(0,1000.)

initial_state = np.array([0.01, 0., 0.])
# initial states of the multiple shoot should be a good guess of the traject
initial_states_matrix=np.zeros((number_of_states,horizon-1))
for i in range(0,horizon-1):
    initial_states_matrix[0,i] = 0.5*(i/(horizon-1))+0.01
    initial_states_matrix[1,i] = 0.1*(i/(horizon-1))
    initial_states_matrix[2, i] = 0

initial_states=np.reshape(initial_states_matrix.T,(number_of_states*(horizon-1),1))

reference_state = np.array([2, 0.5, 0])
reference_input = np.array([0, 0])*0.01

# setup a simulator to test
sim = tools.Simulator(trailer_controller.location)

j=number_of_inputs*horizon
for i in range(0,number_of_states*(horizon-1)):
    sim.set_init_value_solver(initial_states[i],j)
    j+=1

# simulate and get the whole horizon of inputs
(sim_data,full_solution)= sim.simulate_nmpc_multistep_solution(initial_state,reference_state,reference_input,number_of_inputs*horizon+(horizon-1)*number_of_states)
print("solved problem in "+str(sim_data.panoc_interations)+" iterations")

# print("output full simulation")
# print(full_solution)

# calculate the states using these inputs
inputs = np.reshape(full_solution[0:horizon*number_of_inputs],(horizon,number_of_inputs))
print("The optimal inputs are:")
print(inputs)

# get the intermediate states
intermediate_states = np.reshape(full_solution[horizon*number_of_inputs:],(horizon-1,number_of_states))
print("The intermediate states used by the multiple shot are:")
print(intermediate_states)

# use the inputs to simulate the system
state = initial_state
state_history = np.zeros((number_of_states, horizon))
for i in range(0, horizon):
    optimal_input=inputs[i,:].T
    state = model.get_next_state_numpy(state, optimal_input)

    state_history[:, i] = np.reshape(state[:], number_of_states)

plt.figure(0)
example_models.trailer_print(intermediate_states.T,color="r")
example_models.trailer_print(state_history,color="g")
# rectangle.plot()
plt.xlim([0, 2.5])
plt.ylim([0, 0.7])
plt.xlabel('x')
plt.xlabel('y')
plt.title('Trailer parcour')

plt.show()