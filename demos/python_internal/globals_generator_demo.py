import sys
sys.path.insert(0, '../../src_python')
import nmpccodegen as nmpc
import nmpccodegen.tools as tools
import nmpccodegen.models as models
import nmpccodegen.controller as controller
import nmpccodegen.Cfunctions as cfunctions

import numpy as np

def main():
    (system_equations, number_of_states, number_of_inputs, coordinates_indices) = \
        nmpc.example_models.get_trailer_model(L=0.5)

    test_generator = controller.Globals_generator("./test_globals.c")

    step_size=0.1
    integrator = "RK"
    constraint_input = cfunctions.IndicatorBoxFunction([-1, -1], [1, 1])  # input needs stay within these borders
    model = models.Model_continious(system_equations, constraint_input, step_size, number_of_states, \
                                    number_of_inputs, coordinates_indices, integrator)

    Q = np.diag([1., 100., 1.])
    R = np.eye(model.number_of_inputs, model.number_of_inputs) * 1.

    stage_cost = controller.stage_costs.Stage_cost_QR(model, Q, R)

    # define the controller, set the controller on whatever location, as we won't generate code it doesnt matter
    trailer_controller = controller.Nmpc_panoc("./", model, stage_cost)

    test_generator.generate_globals(trailer_controller)

if __name__ == "__main__":
    main()