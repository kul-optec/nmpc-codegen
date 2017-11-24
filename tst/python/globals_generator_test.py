import chainDynCasadi as cdd

# little hack to import the local lib and not work with the one in the path
import sys
sys.path.insert(0, '../../src_python')
import nmpc_panoc as npc
import globals_generator as gg



def main():
    dimension = 2
    number_of_balls = 4  # M
    ball_mass = 0.03  # m
    spring_constant = 0.1  # D
    rest_length_of_springs = 0.033  # L
    gravity_acceleration = 9.81
    model_params = cdd.Chain_dyn_parameters(dimension, number_of_balls, ball_mass,spring_constant, rest_length_of_springs, gravity_acceleration)

    test_generator = gg.Globals_generator("./test_globals.c")

    f = 0
    g = 0
    d = 0
    x_dimension = 0
    u_dimension = 0

    nmpc_controller = npc.Nmpc_panoc("../../", f, g, d, x_dimension, u_dimension)

    test_generator.generate_globals(nmpc_controller)


if __name__ == "__main__":
    main()