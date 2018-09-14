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
import matplotlib.pyplot as plt

def calculate_horizon(trailer_controller,sim,initial_state,reference_state,reference_input,obstacle_weights):
    # -- simulate controller --
    simulation_time = 2
    number_of_steps = math.ceil(simulation_time / trailer_controller.model.step_size)
    # setup the weights on a simulator to test
    for i in range(0,len(obstacle_weights)):
        sim.set_weight_constraint(i, obstacle_weights[i])
    for i in range(0,len(reference_state)*trailer_controller.horizon):
        sim.set_init_value_solver(0.,i)

    state = initial_state
    state_history = np.zeros((trailer_controller.model.number_of_states, trailer_controller.horizon))

    (sim_data, full_solution) = sim.simulate_nmpc_multistep_solution(initial_state, reference_state, reference_input,
                                      trailer_controller.model.number_of_inputs * trailer_controller.horizon)
    print("problem solved in "+str(sim_data.panoc_interations)+" iterations \n")
    inputs = np.reshape(full_solution, (trailer_controller.horizon, trailer_controller.model.number_of_inputs))

    for i in range(0, trailer_controller.horizon):
        state = trailer_controller.model.get_next_state_numpy(state, inputs[i,:].T)
        state_history[:, i] = np.reshape(state[:], trailer_controller.model.number_of_states)

    print("Final state:")
    print(state)

    return state_history

def prepare_demo_trailer(step_size,Q,R,Q_terminal=None,R_terminal=None):
    "construct a simple demo controller"

    # generate static files
    trailer_controller_output_location =  "../../test_controller_builds/demo_controller"
    tools.Bootstrapper.bootstrap(trailer_controller_output_location, simulation_tools=True)

    # get example model from lib
    (system_equations, number_of_states, number_of_inputs, coordinates_indices) = nmpc.example_models.get_trailer_model(
        L=0.5)

    integrator = "RK44"  # select a Runga-Kutta  integrator (FE is forward euler)
    constraint_input = cfunctions.IndicatorBoxFunction([-4, -4], [4, 4])  # input needs stay within these borders
    model = models.Model_continious(system_equations, constraint_input, step_size, number_of_states, \
                                    number_of_inputs, coordinates_indices, integrator)

    # define the contro
    stage_cost = controller.Stage_cost_QR(model, Q, R)
    if(Q_terminal is None):
        trailer_controller = controller.Nmpc_panoc(trailer_controller_output_location, model, stage_cost)
    else:
        terminal_cost = controller.Stage_cost_QR(model, Q_terminal, R_terminal)
        trailer_controller = controller.Nmpc_panoc(trailer_controller_output_location, model, stage_cost,terminal_cost)

    return trailer_controller

def simulate_demo(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights):
    # -- simulate controller --
    simulation_time = 3
    number_of_steps = math.ceil(simulation_time / trailer_controller.model.step_size)
    # setup a simulator to test
    sim = tools.Simulator(trailer_controller.location)
    for i in range(0,len(obstacle_weights)):
        sim.set_weight_constraint(i, obstacle_weights[i])

    state = initial_state
    state_history = np.zeros((trailer_controller.model.number_of_states, number_of_steps))

    for i in range(0, number_of_steps):
        result_simulation = sim.simulate_nmpc(state, reference_state, reference_input)
        print("Step [" + str(i+1) + "/" + str(number_of_steps) + "]: The optimal input is: [" \
              + str(result_simulation.optimal_input[0]) + "," + str(result_simulation.optimal_input[0]) + "]" \
              + " time=" + result_simulation.time_string + " number of panoc iterations=" + str(
            result_simulation.panoc_interations) + " cost=" + str(sim.get_last_buffered_cost()) )

        state = trailer_controller.model.get_next_state_numpy(state, result_simulation.optimal_input)
        state_history[:, i] = np.reshape(state[:], trailer_controller.model.number_of_states)

    print("Final state:")
    print(state)

    return state_history

def draw_obstacle_border(h,xlim,number_of_points):
    x = np.asarray(np.linspace(xlim[0],xlim[1],number_of_points))
    y=np.asarray(np.zeros((number_of_points,1)))

    for i in range(0,number_of_points):
        y[i]=h(x[i])

    plt.plot(x,y)