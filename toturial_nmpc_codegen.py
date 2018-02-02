import sys
sys.path.insert(0, './src_python')
import nmpccodegen as nmpc
import nmpccodegen.tools as tools
import nmpccodegen.models as models
import nmpccodegen.controller as controller
import nmpccodegen.Cfunctions as cfunctions
import nmpccodegen.example_models as example_models

import numpy as np
import matplotlib.pyplot as plt
import math

controller_name="toturial_controller"

## -- GENERATE STATIC FILES --
# start by generating the static files and folder of the controller
location_nmpc_repo = "."
output_locationcontroller = location_nmpc_repo + "/test_controller_builds"
trailer_controller_location = output_locationcontroller + "/" + controller_name + "/"

tools.Bootstrapper.bootstrap(output_locationcontroller, controller_name, python_interface_enabled=True)
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
Q = np.diag([1., 100., 1.])
R = np.eye(model.number_of_inputs, model.number_of_inputs) * 1.

# the stage cost is defined two lines,different kinds of stage costs are available to the user.
stage_cost = controller.Stage_cost_QR(model, Q, R)

# define the controller
trailer_controller = controller.Nmpc_panoc(trailer_controller_location, model, stage_cost)
trailer_controller.horizon = horizon # NMPC parameter
trailer_controller.integrator_casadi = True # optional  feature that can generate the integrating used  in the cost function
trailer_controller.panoc_max_steps = 300 # the maximum amount of iterations the PANOC algorithm is allowed to do.
trailer_controller.min_residual=-3

# add an obstacle, a two dimensional rectangle
# obstacle_weight = 1000.
x_up = 0.8
x_down = 0.2
y_up = 0.4
y_down = 0.2
obstacle = controller.Basic_obstacles.generate_rec_object(x_up, x_down, y_up, y_down)
trailer_controller.add_obstacle(obstacle)

# generate the dynamic code
trailer_controller.generate_code()

# -- simulate controller --
# setup a simulator to test
sim = tools.Simulator(trailer_controller.location)

# init the controller
sim.simulator_init()

sim.set_weight_obstacle(0,1000.)

initial_state = np.array([0.01, 0., 0.])
reference_state = np.array([2, 0.5, 0])
reference_input = np.array([0, 0])
state = initial_state
state_history = np.zeros((number_of_states, number_of_steps))

for i in range(1, number_of_steps):
    result_simulation= sim.simulate_nmpc(state,reference_state,reference_input)
    print("Step ["+str(i)+"/"+str(number_of_steps)+"]: The optimal input is: [" \
          + str(result_simulation.optimal_input[0]) + "," + str(result_simulation.optimal_input[0]) + "]" \
          + " time=" + result_simulation.time_string + " number of panoc iterations=" + str(result_simulation.panoc_interations))

    state = model.get_next_state_numpy(state, result_simulation.optimal_input)
    state_history[:, i] = np.reshape(state[:], number_of_states)
    if i<14 :
        sim.set_weight_obstacle(0,(10**i))

# cleanup the controller
sim.simulator_cleanup()

print("Final state:")
print(state)

plt.figure(0)
example_models.trailer_print(state_history)
example_models.draw_rectangular_obstacle(x_up,x_down,y_up,y_down)
plt.xlim([0, 2.5])
plt.ylim([0, 0.7])
plt.xlabel('x')
plt.xlabel('y')
plt.title('Trailer parcour')
plt.savefig(controller_name + '.png')
plt.show()