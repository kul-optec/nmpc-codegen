import sys
sys.path.insert(0, './src_python')
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
import sys
import time
import obstacle as obs

controller_name="toturial_controller"

## -- GENERATE STATIC FILES --
# start by generating the static files and folder of the controller
location_nmpc_repo = "."
output_locationcontroller = location_nmpc_repo + "/test_controller_builds"
trailer_controller_location = output_locationcontroller + "/" + controller_name + "/"

bs.Bootstrapper_panoc_nmpc.bootstrap(location_nmpc_repo, output_locationcontroller, controller_name, python_interface_enabled=True)
## -----------------------------------------------------------------

# get the continuous system equations from the existing library
(system_equations, number_of_states, number_of_inputs, coordinates_indices) = example_models.get_trailer_model(
    L=0.5)

step_size = 0.05
simulation_time = 10
number_of_steps = math.ceil(simulation_time / step_size)
horizon = 10

integrator = "RK" # select a Runga-Kutta  integrator
constraint_input = indbox.IndicatorBoxFunction([-1, -1], [1, 1])  # input needs stay within these borders
model = modelc.Model_continious(system_equations, constraint_input, step_size, number_of_states, \
                                number_of_inputs, coordinates_indices, integrator)

# Q and R matrixes determined by the control engineer.
Q = np.diag([1., 100., 1.])
R = np.eye(model.number_of_inputs, model.number_of_inputs) * 1.

# the stage cost is defined two lines,different kinds of stage costs are available to the user.
reference_state = np.array([2, 0.5, 0])
stage_cost = stage_costs.Stage_cost_QR_reference(model, Q, R, reference_state)

# define the controller
trailer_controller = npc.Nmpc_panoc(trailer_controller_location, model, stage_cost)
trailer_controller.horizon = horizon # NMPC parameter
trailer_controller.integrator_casadi = True # optional  feature that can generate the integrating used  in the cost function
trailer_controller.panoc_max_steps = 500 # the maximum amount of iterations the PANOC algorithm is allowed to do.

# add an obstacle, a two dimensional rectangle
obstacle_weight = 10000000000000.
x_up = 1.
x_down = 0.5
y_up = 0.4
y_down = 0.2
obstacle = obs.Basic_obstacles.generate_rec_object(x_up, x_down, y_up, y_down)
trailer_controller.add_obstacle(obstacle, obstacle_weight)

# generate the dynamic code
trailer_controller.generate_code()

# -- simulate controller --
# setup a simulator to test
sim = simulator.Simulator(trailer_controller)

# init the controller
sim.simulator_init()

initial_state = np.array([0.01, 0., 0.])
state = initial_state
state_history = np.zeros((number_of_states, number_of_steps))

for i in range(1, number_of_steps):
    result_simulation= sim.simulate_nmpc(state)
    print("Step ["+str(i)+"/"+str(number_of_steps)+"]: The optimal input is: [" \
          + str(result_simulation.optimal_input[0]) + "," + str(result_simulation.optimal_input[0]) + "]" \
          + " time=" + result_simulation.time_string)

    state = np.asarray(model.get_next_state(state, result_simulation.optimal_input))
    state_history[:, i] = np.reshape(state[:], number_of_states)

# cleanup the controller
sim.simulator_cleanup()

print("Final state:")
print(state)

plt.figure(1)
plt.subplot(211)
plt.plot(state_history[0, :], state_history[1, :])
plt.subplot(212)
plt.plot(state_history[2, :])
plt.show()
plt.savefig(controller_name + '.png')
plt.clf()
sys.stdout.flush()