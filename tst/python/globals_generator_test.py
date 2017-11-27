import chainDynCasadi as cdd

# little hack to import the local lib and not work with the one in the path
import sys
sys.path.insert(0, '../../src_python')
import nmpc_panoc as npc
import globals_generator as gg
import numpy as np
import model_continious as modelc


def main():
    dimension = 2
    number_of_balls = 4  # M
    ball_mass = 0.03  # m
    spring_constant = 0.1  # D
    rest_length_of_springs = 0.033  # L
    gravity_acceleration = 9.81
    model_params = cdd.Chain_dyn_parameters(dimension, number_of_balls, ball_mass,spring_constant, rest_length_of_springs, gravity_acceleration)

    test_generator = gg.Globals_generator("./test_globals.c")

    number_of_states=model_params.number_of_states
    number_of_inputs=model_params.dimension
    step_size=0.1


    f = 0
    g = 0
    d = 0
    x_dimension = 0
    u_dimension = 0

    model = modelc.Model_continious(f, g,step_size,number_of_states,number_of_inputs, integrator="RK")

    Q = np.eye(number_of_states, number_of_states)
    R = np.eye(number_of_inputs, number_of_inputs)
    nmpc_controller = npc.Nmpc_panoc("../../", model, Q, R)

    test_generator.generate_globals(nmpc_controller)


if __name__ == "__main__":
    main()