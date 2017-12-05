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


# simulation_cleanup
def main():
    model = example_models.get_chain_model()
    dimension = 2
    number_of_balls=4

    Q = np.diag([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1])
    R = np.eye(model.number_of_inputs, model.number_of_inputs)*10

    nmpc_controller = npc.Nmpc_panoc("../../", model, Q, R)
    nmpc_controller.horizon = 50
    nmpc_controller.step_size=0.1

    nmpc_controller.generate_code()

    rest_state = np.array([0.1932, -5.9190, 0.3874, -8.8949, 0.6126, -8.8949, 0.8068, -5.9190 \
                              , 1., 0., \
                           0., 0., 0., 0., 0., 0., 0., 0.])
    current_state = [ 0.2, 0. , 0.4,0. , 0.6 , 0. , 0.8 , 0. \
                    ,1. , 0., \
                    0.,0., 0.,0.,0.,0.,0.,0. ]

    # setup a simulator to test
    sim = simulator.Simulator('../../')

    # init the controller
    sim.simulator_init()

    number_of_steps=10
    for i in range(1,number_of_steps):
        (test,optimal_input) = sim.simulate_nmpc(current_state,2)
        print("The optimal input is: [" + str(optimal_input[0]) + "," + str(optimal_input[0]) + "]")
        current_state = model.get_next_state(current_state, optimal_input)

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