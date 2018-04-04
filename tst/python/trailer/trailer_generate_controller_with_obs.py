import sys
sys.path.insert(0, '../../../src_python')
import nmpccodegen as nmpc
import nmpccodegen.tools as tools
import nmpccodegen.models as models
import nmpccodegen.controller as controller
import nmpccodegen.controller.obstacles as obstacles
import nmpccodegen.Cfunctions as cfunctions
import nmpccodegen.example_models as example_models

import math
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import time

def init_controller_files(controller_name):
    ## -- GENERATE STATIC FILES --
    # start by generating the static files and folder of the controller
    trailer_controller_location = "../../../test_controller_builds/" + controller_name
    tools.Bootstrapper.bootstrap(trailer_controller_location, simulation_tools=True)
    return trailer_controller_location
    ## -----------------------------------------------------------------

def generate_controller_with_obs(trailer_controller_location,reference_state,Q,R,rectangular_obstacle_1,obstacle_weight,horizon,display_figure=True,index_figure=0):

    # get the continious system equations
    (system_equations,number_of_states,number_of_inputs,coordinates_indices) = example_models.get_trailer_model(L=0.5)

    step_size = 0.05
    # simulation_time = 10
    # number_of_steps = math.ceil(simulation_time / step_size)

    integrator = "RK44"
    constraint_input = cfunctions.IndicatorBoxFunction([-1,-1],[1,1]) # input needs stay within these borders
    model = models.Model_continious(system_equations, constraint_input, step_size, number_of_states,\
                                    number_of_inputs,coordinates_indices, integrator)

    # reference_state=np.array([2,2,0])
    stage_cost = controller.Stage_cost_QR(model, Q, R)

    # define the controller
    trailer_controller = controller.Nmpc_panoc(trailer_controller_location,model,stage_cost)
    trailer_controller.horizon = horizon
    trailer_controller.step_size = step_size
    trailer_controller.integrator_casadi = True
    trailer_controller.panoc_max_steps= 1000
    trailer_controller._lbgfs_buffer_size = 20
    trailer_controller.min_residual = -5

    # add an obstacle
    trailer_controller.add_obstacle(rectangular_obstacle_1)

    # generate the code
    trailer_controller.generate_code()

    # -- simulate controller --
    # setup a simulator to test
    sim = tools.Simulator(trailer_controller.location)


    initial_state=np.array([0.01,0.,0.])
    state=initial_state
    state_history = np.zeros((number_of_states,horizon))

    sim.set_weight_obstacle(0,obstacle_weight)
    reference_input = np.array([0, 0])

    (sim_data, full_solution) = sim.simulate_nmpc_multistep_solution(initial_state, reference_state, reference_input,
                                      number_of_inputs * horizon)
    inputs = np.reshape(full_solution, (horizon, number_of_inputs))

    print("solved NMPC problem time="+ sim_data.time_string + " number of panoc iterations=" + str(
        sim_data.panoc_interations))
    for i in range(0,horizon):
        state = model.get_next_state_numpy(state,inputs[i,:])
        state_history[:,i] = np.reshape(state[:],number_of_states)

    print("Reference state:")
    print(reference_state)
    print("Final state:")
    print(state)

    if(display_figure==True):
        plt.figure(index_figure)
        example_models.trailer_print(state_history)
        rectangular_obstacle_1.plot()
        plt.xlim([-2.2, 2.2])
        plt.ylim([-0.1, 2.2])
        # plt.clf()

    return state

def main():
    # create static files
    trailer_move_diag_obs_location_ = init_controller_files("trailer_move_diag_obs")
    trailer_move_right_obs_location_ = init_controller_files("trailer_move_right_obs")
    trailer_move_move_up_obs_location_ = init_controller_files("trailer_move_up_obs")

    # Start simulating:

    # TEST 1
    rectangular_center_coordinates = np.array([0.75, 0.45])
    rectangular_width = 0.5
    rectangular_height = 0.3
    rectangular_obstacle_1 = obstacles.Obstacle_rectangular(rectangular_center_coordinates, \
                                                 rectangular_width, rectangular_height)


    Q = np.diag([10., 10., 1.])
    R = np.diag([1., 1.]) * 0.01
    obstacle_weight = 10000.
    horizon = 50

    reference_state = np.array([2, 0.5, 0])
    current_state = generate_controller_with_obs(trailer_move_diag_obs_location_, reference_state, Q,R, \
                                                 rectangular_obstacle_1 , obstacle_weight,\
                                                 horizon,display_figure=True,index_figure=0)

    # TEST 2
    rectangular_center_coordinates_2 = np.array([1, 0.])
    rectangular_width_2 = 0.5
    rectangular_height_2 = 0.2
    rectangular_obstacle_2 = obstacles.Obstacle_rectangular(rectangular_center_coordinates_2, \
                                                            rectangular_width_2, rectangular_height_2)

    Q = np.diag([10., 10., 1.])*1.
    R = np.diag([1., 1.]) * 0.01
    obstacle_weight = 1000.
    horizon = 50

    reference_state = np.array([2, 0, 0])
    current_state = generate_controller_with_obs(trailer_move_right_obs_location_, reference_state, Q, R,\
                                          rectangular_obstacle_2,obstacle_weight,horizon,\
                                          display_figure=True,index_figure=1)



    # TEST 3
    rectangular_center_coordinates = np.array([0.6, 0.5])
    rectangular_width = 1.2
    rectangular_height = 0.2
    rectangular_obstacle_3 = obstacles.Obstacle_rectangular(rectangular_center_coordinates, \
                                                            rectangular_width, rectangular_height)

    Q = np.diag([10., 10., 0.1])
    R = np.diag([1., 1.]) * 0.01
    obstacle_weight = 10000.
    horizon = 50

    reference_state = np.array([0, 2, 0])
    current_state = generate_controller_with_obs(trailer_move_move_up_obs_location_, reference_state, Q, R,\
                                             rectangular_obstacle_3,obstacle_weight,horizon,\
                                             display_figure=True,index_figure=2)

    plt.show()
if __name__ == '__main__':
    main()
