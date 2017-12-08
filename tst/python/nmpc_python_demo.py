# little hack to import the local lib and not work with the one in the path
import sys
sys.path.insert(0, '../../src_python')
import nmpc_panoc as npc
import model_continious as modelc
import example_models # this contains the chain example

import ctypes
import simulator
import numpy as np
import matplotlib.pyplot as plt
import math
import Cfunctions.IndicatorBoxFunction as indbox
import bootstrapper as bs

# simulation_cleanup
def main():
    # start by generating the static files and folder of the controller
    location_nmpc_repo = "../.."
    location = location_nmpc_repo + "/test_controller_builds"
    controller_name = "nmpc_python_demo"
    nmpc_controller_location=location+"/"+ controller_name + "/"

    bs.Bootstrapper_panoc_nmpc.bootstrap(location_nmpc_repo, location, controller_name,python_interface_enabled=True)

    # get an example model
    (system_equations, number_of_states, number_of_inputs) = example_models.get_chain_model()
    dimension = 2
    number_of_balls = 4

    step_size = 0.01
    simulation_time = 5
    number_of_steps = math.ceil(simulation_time / step_size)

    integrator = "RK"
    constraint_input = indbox.IndicatorBoxFunction([-2,-2],[2,2]) # input needs stay within these borders
    model = modelc.Model_continious(system_equations, constraint_input, step_size, number_of_states,\
                                    number_of_inputs, integrator)


    Q = np.diag([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1])
    R = np.eye(model.number_of_inputs, model.number_of_inputs)*10

    # define the controller
    nmpc_controller = npc.Nmpc_panoc(nmpc_controller_location, model, Q, R)
    nmpc_controller.horizon = 50
    nmpc_controller.step_size=0.1
    nmpc_controller.integrator_casadi = True

    # generate the code
    nmpc_controller.generate_code()

    # From here of on , only simulation !
    #

    rest_state = np.array([0.1932, -5.9190, 0.3874, -8.8949, 0.6126, -8.8949, 0.8068, -5.9190 \
                              , 1., 0., \
                           0., 0., 0., 0., 0., 0., 0., 0.])
    current_state =  np.array([ 0.2, 0. , 0.4,0. , 0.6 , 0. , 0.8 , 0. \
                    ,1. , 0., \
                    0.,0., 0.,0.,0.,0.,0.,0. ]).reshape(model.number_of_states,1)

    # setup a simulator to test
    sim = simulator.Simulator(nmpc_controller)

    # init the controller
    sim.simulator_init()

    number_of_steps=100
    for i in range(1,number_of_steps):
        (test,optimal_input) = sim.simulate_nmpc(current_state)
        print("The optimal input is: [" + str(optimal_input[0]) + "," + str(optimal_input[0]) + "]")
        current_state = np.asarray(model.get_next_state(current_state, optimal_input))

    # cleanup the controller
    sim.simulator_cleanup()

    # display the end result
    final_positions = np.concatenate(\
        (np.zeros((dimension,1)),np.reshape(current_state[0:dimension*(number_of_balls+1)],(number_of_balls+1,dimension)).T)\
    ,axis=1)

    print(current_state)
    print(final_positions)

    plt.plot(final_positions[0,:],final_positions[1,:])
    plt.show()


if __name__ == "__main__":
    main()