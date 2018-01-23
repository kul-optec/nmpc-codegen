import sys
sys.path.insert(0, '../../../src_python')
import nmpccodegen as nmpc
import nmpccodegen.tools as tools
import nmpccodegen.models as models
import nmpccodegen.controller as controller
import nmpccodegen.Cfunctions as cfunctions

import math
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import time

def generate_controller(controller_name,reference_state,display_figure=True):
    ## -- GENERATE STATIC FILES --
    # start by generating the static files and folder of the controller
    location_nmpc_repo = "../../.."
    location = location_nmpc_repo + "/test_controller_builds"
    # controller_name = "trailer_simple_controller"
    trailer_controller_location=location+"/"+ controller_name + "/"

    tools.Bootstrapper.bootstrap(location, controller_name,python_interface_enabled=True)
    ## -----------------------------------------------------------------

    # get the continious system equations
    (system_equations,number_of_states,number_of_inputs,coordinates_indices) = nmpc.example_models.get_trailer_model(L=0.5)

    step_size = 0.05
    simulation_time = 10
    number_of_steps = math.ceil(simulation_time / step_size)

    integrator = "RK"
    constraint_input = cfunctions.IndicatorBoxFunction([-1,-1],[1,1]) # input needs stay within these borders
    model = models.Model_continious(system_equations, constraint_input, step_size, number_of_states,\
                                    number_of_inputs,coordinates_indices, integrator)

    Q = np.diag([1.,100.,1.])
    R = np.eye(model.number_of_inputs, model.number_of_inputs)*1.

    # reference_state=np.array([2,2,0])
    stage_cost = controller.stage_costs.Stage_cost_QR_reference(model,Q,R,reference_state)

    # define the controller
    trailer_controller = controller.Nmpc_panoc(trailer_controller_location,model,stage_cost )
    trailer_controller.horizon = 100
    trailer_controller.step_size = step_size
    trailer_controller.integrator_casadi = True
    trailer_controller.panoc_max_steps=100000
    trailer_controller._lbgfs_buffer_size = 50

    # generate the code
    trailer_controller.generate_code()

    # -- simulate controller --
    # setup a simulator to test
    sim = tools.Simulator(trailer_controller)

    # init the controller
    sim.simulator_init()

    initial_state=np.array([0.01,0.,0.])
    state=initial_state
    state_history = np.zeros((number_of_states,number_of_steps))

    for i in range(1,number_of_steps):
        result_simulation = sim.simulate_nmpc(state)
        print("Step [" + str(i) + "/" + str(number_of_steps) + "]: The optimal input is: [" \
              + str(result_simulation.optimal_input[0]) + "," + str(result_simulation.optimal_input[0]) + "]" \
              + " time=" + result_simulation.time_string + " number of panoc iterations=" + str(
            result_simulation.panoc_interations))
        sys.stdout.flush()

        state = np.asarray(model.get_next_state(state,result_simulation.optimal_input))
        state_history[:,i] = np.reshape(state[:],number_of_states)

    # cleanup the controller
    sim.simulator_cleanup()

    print("Final state:")
    print(state)

    if(display_figure==True):
        plt.figure(1)
        plt.subplot(211)
        plt.plot(state_history[0,:],state_history[1,:])
        plt.subplot(212)
        plt.plot(state_history[2,:])
        plt.show()
        plt.savefig(controller_name+'.png')
        plt.clf()
        sys.stdout.flush()

    return state

def main():
   reference_state=np.array([0,2,0])
   current_state = generate_controller("trailer_move_up",reference_state)

   reference_state=np.array([2,0,0])
   current_state = generate_controller("trailer_move_right",reference_state)

   reference_state=np.array([2,2,0])
   current_state = generate_controller("trailer_move_diag",reference_state)
if __name__ == '__main__':
    main()
