import models.chain_model as cm
import numpy as np
import math
import model_continious as modelc
import Cfunctions.IndicatorBoxFunction as indbox

def get_chain_model():
    # model parameters(use the same as the Matlab code):
    dimension = 2
    number_of_balls = 4  # M
    ball_mass = 0.03  # m
    spring_constant = 0.1  # D
    rest_length_of_springs = 0.033  # L
    gravity_acceleration = 9.81

    model_params = cm.Chain_dyn_parameters(dimension, number_of_balls, ball_mass, spring_constant,
                                            rest_length_of_springs, gravity_acceleration)

    system_equations = lambda state, input: cm.chain_dyn(state, input, model_params)

    number_of_states = model_params.number_of_states
    number_of_inputs = model_params.dimension

    return (system_equations,number_of_states,number_of_inputs)