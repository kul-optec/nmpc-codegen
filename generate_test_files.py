# import numpy as np

import sys
sys.path.insert(0, './src_python')
import nmpccodegen as nmpc
import nmpccodegen.tools as tools
import nmpccodegen.models as models
import nmpccodegen.controller as controller
import nmpccodegen.Cfunctions as cfunctions

import math
import casadi as cd
import numpy as np

def main():
    (system_equations, number_of_states, number_of_inputs,indices_coordinates) = nmpc.example_models.get_chain_model()
    dimension = 2
    number_of_balls = 4

    step_size = 0.01
    simulation_time = 5
    number_of_steps = math.ceil(simulation_time / step_size)

    integrator = "RK44"
    constraint_input = cfunctions.IndicatorBoxFunction([-2, -2], [2, 2])  # input needs stay within these borders
    model = models.Model_continious(system_equations, constraint_input, step_size, number_of_states, \
                                    number_of_inputs,indices_coordinates, integrator)

    # Q = np.eye(model.number_of_states, model.number_of_states)
    Q = np.diag([0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])*10
    R = np.eye(model.number_of_inputs, model.number_of_inputs)

    # reference_state=np.array([2,2,0])
    stage_cost = controller.Stage_cost_QR(model, Q, R)

    # define the controller
    controller_location = "./"
    nmpc_controller = controller.Nmpc_panoc(controller_location,model,stage_cost )

    nmpc_controller.horizon = 50
    nmpc_controller.step_size = 0.1

    # add the optional integrator, very useful to debug the code
    nmpc_controller.integrator_casadi=True

    nmpc_controller.generate_code()

if __name__ == "__main__":
    main()