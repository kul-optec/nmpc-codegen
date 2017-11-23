# import numpy as np
import casadi as cd
import numpy as np
import sys
sys.path.insert(0, '../../src_python')
from integrators import *

class Chain_dyn_parameters:
    """ chain dynamic model parameters """

    def __init__(self, dimension, number_of_balls, ball_mass, spring_constant,
                 rest_length_of_springs, gravity_acceleration):
        self._dimension = dimension  # dim
        self._number_of_balls = number_of_balls  # M
        self._ball_mass = ball_mass  # m
        self._spring_constant = spring_constant  # D
        self._rest_length_of_springs = rest_length_of_springs  # L
        self._gravity_acceleration = gravity_acceleration  # g

    @property
    def dimension(self):
        return self._dimension

    @property
    def number_of_balls(self):
        return self._number_of_balls

    @property
    def ball_mass(self):
        return self._ball_mass

    @property
    def spring_constant(self):
        return self._spring_constant

    @property
    def rest_length_of_springs(self):
        return self._rest_length_of_springs

    @property
    def gravity_acceleration(self):
        return self._gravity_acceleration

    # properties calculated based on model parameters
    @property
    def number_of_states(self):
        return self._dimension * (2 * self._number_of_balls + 1)

    @property
    def number_of_inputs(self):
        return self._dimension * (2 * self._number_of_balls + 1)

    @property
    def number_of_outputs(self):
        return self._dimension * (2 * self._number_of_balls + 1)


# x: state vector [pos_1, ..., pos_M, pos_{M+1}, vel_1, ..., vel_M]
# u: input vector
def chain_dyn(x, u, model_parameters):
    """ returns the derivative of the state dx=f(x) """

    positions = cd.reshape(x[0:model_parameters.dimension * (model_parameters.number_of_balls + 1), 0], \
                            ( model_parameters.dimension,model_parameters.number_of_balls + 1) \
                            )
    velocities=cd.reshape(\
            x[model_parameters.dimension * (model_parameters.number_of_balls + 1):, 0], \
            (model_parameters.dimension,model_parameters.number_of_balls)\
        )

    # compute distance between masses
    distance_between_balls = \
        positions[0:model_parameters.dimension, 1:model_parameters.number_of_balls + 1 ] - \
        positions[0:model_parameters.dimension, 0:model_parameters.number_of_balls ]

    # add the distance(and its norm) between the first ball and the fixed wall
    distance_between_balls = cd.horzcat(
        positions[0:model_parameters.dimension, 0],distance_between_balls \
        )
    distance_between_balls_norm = cd.sqrt(cd.sum1(distance_between_balls ** 2))

    # calculate force between balls on springs
    F = model_parameters.spring_constant * (1 - model_parameters.rest_length_of_springs / \
                                            cd.repmat(distance_between_balls_norm,model_parameters.dimension,1) )\
        * distance_between_balls


    gravitational_force = np.concatenate(\
                                    (\
                                     np.zeros((1,model_parameters.number_of_balls)), \
                                     -np.ones((1,model_parameters._number_of_balls))*model_parameters.gravity_acceleration \
                                    ) \
                                    ,axis=0)

    # find acceleration
    acceleration = (1 / model_parameters.ball_mass) * \
                   (F[:, 1:] - F[:, 0:model_parameters.number_of_balls]) \
                   + gravitational_force

    x_dot = cd.horzcat(velocities,u, acceleration)

    return cd.reshape(x_dot,(model_parameters.number_of_outputs,1))

def main():
    print("Simple demo chain dynamics with 5 masses:")
    # model parameters:
    dimension = 2
    number_of_balls = 5
    ball_mass = 1
    spring_constant = 1
    rest_length_of_springs = 2
    gravity_acceleration = 9.81

    model_params = Chain_dyn_parameters(dimension, number_of_balls, ball_mass,
                                        spring_constant, rest_length_of_springs, gravity_acceleration)

    # import inspect
    # all_functions = inspect.getmembers(cd, inspect.isfunction)
    # print(all_functions)
    # # initial state:
    # x0 = cd.array([1., 0., 2., 0., 3., 0., 4., 0., 5., 0., 6., 0., 0., 0., 0., 0., 0.])
    x = cd.SX.sym( 'x', 22 ,1 )
    # x0 = x0.T
    # u0 = cd.array([6, 0])
    u = cd.SX.sym( 'u', 2 ,1 )

    #
    # # call the chain dyn function with intial state
    # x0_dot = chain_dyn(x, u, model_params)
    f = cd.Function('f',[x,u],[chain_dyn(x, u, model_params)])

    x0 = np.array([1., 0., 2., 0., 3., 0., 4., 0., 5., 0., 6., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
    x0 = x0.T
    u0 = np.array([6, 0])
    test = f(x0,u0)
    print(test)

if __name__ == "__main__":
    main()