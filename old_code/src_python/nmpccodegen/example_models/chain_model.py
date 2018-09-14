import casadi as cd
import numpy as np

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
    a=3
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