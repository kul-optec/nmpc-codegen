import sys
sys.path.insert(0, '../../src_python')
import nmpccodegen as nmpc
import nmpccodegen.tools as tools
import nmpccodegen.models as models
import nmpccodegen.controller as controller
import nmpccodegen.controller.obstacles as obstacles
import nmpccodegen.Cfunctions as cfunctions
import nmpccodegen.example_models as example_models

import numpy as np
import matplotlib.pyplot as plt
import math

from demo import prepare_demo_trailer,simulate_demo

def calculate_horizon(trailer_controller,sim,initial_state,reference_state,reference_input,obstacle_weights):
    # -- simulate controller --
    simulation_time = 2
    number_of_steps = math.ceil(simulation_time / trailer_controller.model.step_size)
    # setup the weights on a simulator to test
    for i in range(0,len(obstacle_weights)):
        sim.set_weight_obstacle(i, obstacle_weights[i])
    # TODO set the initial position !

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

if __name__ == '__main__':
    step_size=0.05

    # Q and R matrixes determined by the control engineer.
    Q = np.diag([1., 1., 0.01])*0.2
    R = np.diag([1., 1.]) * 0.01

    trailer_controller = prepare_demo_trailer(step_size,Q,R)

    trailer_controller.horizon = 30 # NMPC parameter
    trailer_controller.integrator_casadi = True # optional  feature that can generate the integrating used  in the cost function
    trailer_controller.panoc_max_steps = 500 # the maximum amount of iterations the PANOC algorithm is allowed to do.
    trailer_controller.min_residual=-3

    # construct lower rectangular
    rectangular_center_coordinates = np.array([2,0.5])
    rectangular_width = 0.4
    rectangular_height = 0.4
    rectangular_obstacle = obstacles.Obstacle_rectangular(rectangular_center_coordinates,\
                                                 rectangular_width,rectangular_height)

    circular_obstacle = obstacles.Obstacle_circle(rectangular_center_coordinates,0.5)

    # add obstacles to controller
    trailer_controller.add_obstacle(circular_obstacle)

    # generate the dynamic code
    trailer_controller.generate_code()

    # simulate everything
    initial_state = np.array([0., 0.5,0])
    reference_state = np.array([3, 0.5, 0])
    reference_input = np.array([0, 0])   

    sim = tools.Simulator(trailer_controller.location)

    obstacle_weights = [10.,10.,10.]
    state_history_1 = calculate_horizon(trailer_controller,sim,initial_state,reference_state,reference_input,obstacle_weights)
    obstacle_weights = [10.**3,10.**3,10.**3]
    state_history_2 = calculate_horizon(trailer_controller,sim,initial_state,reference_state,reference_input,obstacle_weights)
    obstacle_weights = [10.**9,10.**9,10.**9]
    state_history_3 = calculate_horizon(trailer_controller,sim,initial_state,reference_state,reference_input,obstacle_weights)


    plt.figure(0)
    example_models.trailer_print(state_history_1,'k')
    example_models.trailer_print(state_history_2,'r')
    example_models.trailer_print(state_history_3,'g')
    # rectangular_obstacle.plot()
    circular_obstacle.plot()
    plt.xlim([-0.1, 4])
    plt.ylim([-0.1, 4])
    plt.xlabel('x')
    plt.xlabel('y')
    plt.title('Trailer')
    plt.show()