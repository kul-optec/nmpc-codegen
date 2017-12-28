import sys
sys.path.insert(0, '../../../src_python')
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



def generate_controller(controller_name,reference_state):
    ## -- GENERATE STATIC FILES --
    # start by generating the static files and folder of the controller
    location_nmpc_repo = "../../.."
    location = location_nmpc_repo + "/test_controller_builds"
    # controller_name = "trailer_simple_controller"
    trailer_controller_location=location+"/"+ controller_name + "/"

    bs.Bootstrapper_panoc_nmpc.bootstrap(location_nmpc_repo, location, controller_name,python_interface_enabled=True)
    ## -----------------------------------------------------------------

    # get the continious system equations
    (system_equations,number_of_states,number_of_inputs) = example_models.get_trailer_model(L=0.5)

    step_size = 0.05
    simulation_time = 10
    number_of_steps = math.ceil(simulation_time / step_size)

    integrator = "RK"
    constraint_input = indbox.IndicatorBoxFunction([-1,-1],[1,1]) # input needs stay within these borders
    model = modelc.Model_continious(system_equations, constraint_input, step_size, number_of_states,\
                                    number_of_inputs, integrator)

    Q = np.diag([1,100,1])*100
    R = np.eye(model.number_of_inputs, model.number_of_inputs)*0.

    # reference_state=np.array([2,2,0])
    stage_cost = stage_costs.Stage_cost_QR_reference(model,Q,R,reference_state)

    # define the controller
    trailer_controller = npc.Nmpc_panoc(trailer_controller_location,model,stage_cost )
    trailer_controller.horizon = 100
    trailer_controller.step_size = step_size
    trailer_controller.integrator_casadi = True
    trailer_controller.panoc_max_steps=100

    # generate the code
    trailer_controller.generate_code()

    # -- simulate controller --
    # setup a simulator to test
    sim = simulator.Simulator(trailer_controller)

    # init the controller
    sim.simulator_init()

    initial_state=np.array([0.,0.,0.])
    state=initial_state
    state_history = np.zeros((number_of_states,number_of_steps))

    for i in range(1,number_of_steps):
        (test, optimal_input) = sim.simulate_nmpc(state)
        print("The optimal input is: [" + str(optimal_input[0]) + "," + str(optimal_input[0]) + "]")
        sys.stdout.flush()

        state = np.asarray(model.get_next_state(state,optimal_input))
        state_history[:,i] = np.reshape(state[:],number_of_states)

    # cleanup the controller
    sim.simulator_cleanup()

    print(state)

    plt.figure(1)
    plt.subplot(211)
    plt.plot(state_history[0,:],state_history[1,:])
    plt.subplot(212)
    plt.plot(state_history[2,:])
    # plt.show()
    plt.savefig(controller_name+'.png')
    plt.clf()
    sys.stdout.flush()

def main():
   reference_state=np.array([0,2,0])
   generate_controller("trailer_move_up",reference_state)

   reference_state=np.array([2,0,0])
   generate_controller("trailer_move_right",reference_state)

   reference_state=np.array([2,2,0])
   generate_controller("trailer_move_diag",reference_state)
if __name__ == '__main__':
    main()
