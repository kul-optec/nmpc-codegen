# import numpy as np
import casadi as cd
import numpy as np
import sys
sys.path.insert(0, './src_python')
import nmpc_panoc as npc
import math
import model_continious as modelc
import example_models # this contains the chain example
import math
import Cfunctions.IndicatorBoxFunction as indbox


def main():
    (system_equations, number_of_states, number_of_inputs) = example_models.get_chain_model()
    dimension = 2
    number_of_balls = 4

    step_size = 0.01
    simulation_time = 5
    number_of_steps = math.ceil(simulation_time / step_size)

    integrator = "RK"
    constraint_input = indbox.IndicatorBoxFunction([-2, -2], [2, 2])  # input needs stay within these borders
    model = modelc.Model_continious(system_equations, constraint_input, step_size, number_of_states, \
                                    number_of_inputs, integrator)

    # Q = np.eye(model.number_of_states, model.number_of_states)
    Q = np.diag([0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])*10
    R = np.eye(model.number_of_inputs, model.number_of_inputs)

    nmpc_controller = npc.Nmpc_panoc("./", model, Q, R)

    nmpc_controller.horizon = 50
    nmpc_controller.step_size = 0.1

    nmpc_controller.integrator_casadi=True

    nmpc_controller.generate_code()

if __name__ == "__main__":
    main()