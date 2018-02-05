import sys
sys.path.insert(0, '../../src_python')
import nmpccodegen as nmpc
import nmpccodegen.tools as tools
import nmpccodegen.models as models
import nmpccodegen.controller as controller
import nmpccodegen.Cfunctions as cfunctions
import nmpccodegen.example_models as example_models

import numpy as np
import math

def prepare_demo_trailer(step_size,Q,R):
    "construct a simple demo controller"

    # generate static files
    trailer_controller_output_location =  "../../test_controller_builds/demo_controller"
    tools.Bootstrapper.bootstrap(trailer_controller_output_location, python_interface_enabled=True)

    # get example model from lib
    (system_equations, number_of_states, number_of_inputs, coordinates_indices) = nmpc.example_models.get_trailer_model(
        L=0.5)

    integrator = "RK44"  # select a Runga-Kutta  integrator (FE is forward euler)
    constraint_input = cfunctions.IndicatorBoxFunction([-4, -4], [4, 4])  # input needs stay within these borders
    model = models.Model_continious(system_equations, constraint_input, step_size, number_of_states, \
                                    number_of_inputs, coordinates_indices, integrator)

    # the stage cost is defined two lines,different kinds of stage costs are available to the user.
    stage_cost = controller.Stage_cost_QR(model, Q, R)

    # define the controller
    trailer_controller = controller.Nmpc_panoc(trailer_controller_output_location, model, stage_cost)

    return trailer_controller

def simulate_demo(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights):
    # -- simulate controller --
    simulation_time = 2
    number_of_steps = math.ceil(simulation_time / trailer_controller.model.step_size)
    # setup a simulator to test
    sim = tools.Simulator(trailer_controller.location)
    for i in range(0,len(obstacle_weights)):
        sim.set_weight_obstacle(i, obstacle_weights[i])

    state = initial_state
    state_history = np.zeros((trailer_controller.model.number_of_states, number_of_steps))

    for i in range(0, number_of_steps):
        result_simulation = sim.simulate_nmpc(state, reference_state, reference_input)
        print("Step [" + str(i+1) + "/" + str(number_of_steps) + "]: The optimal input is: [" \
              + str(result_simulation.optimal_input[0]) + "," + str(result_simulation.optimal_input[0]) + "]" \
              + " time=" + result_simulation.time_string + " number of panoc iterations=" + str(
            result_simulation.panoc_interations))

        state = trailer_controller.model.get_next_state_numpy(state, result_simulation.optimal_input)
        state_history[:, i] = np.reshape(state[:], trailer_controller.model.number_of_states)

    print("Final state:")
    print(state)

    return state_history