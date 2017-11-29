# import numpy as np
import casadi as cd
import numpy as np
import sys
sys.path.insert(0, './src_python')
import nmpc_panoc as npc
import math
import model_continious as modelc
import example_models # this contains the chain example


def main():
    model = example_models.get_chain_model()

    # Q = np.eye(model.number_of_states, model.number_of_states)
    Q = np.diag([0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])*10
    R = np.eye(model.number_of_inputs, model.number_of_inputs)

    # the horizon is 10

    nmpc_controller = npc.Nmpc_panoc("./", model, Q, R)
    nmpc_controller.generate_code()

if __name__ == "__main__":
    main()