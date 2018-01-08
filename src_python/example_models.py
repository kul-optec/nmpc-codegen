import models.chain_model as cm
import models.trailer_model as tm
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

    # X = [x^1 ... x^{M+1} u ]
    indices_coordinates=np.arange(0,dimension*(number_of_balls+1))

    return (system_equations,number_of_states,number_of_inputs,indices_coordinates)

def get_trailer_model(L):
    number_of_states=3
    number_of_inputs=2
    indices_coordinates = [0,1] # only x and y are coordinates, theta has nothing to do with position of the trailer
    trailer_model = tm.Trailer_model(L)

    system_equations = lambda state,input: trailer_model.system_equation(state,input)

    return (system_equations,number_of_states,number_of_inputs,indices_coordinates)