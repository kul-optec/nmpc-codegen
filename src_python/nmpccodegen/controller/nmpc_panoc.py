import casadi as cd
import numpy as np
import os
from pathlib import Path

from .globals_generator import Globals_generator
from .casadi_code_generator import Casadi_code_generator as ccg
from .nmpc_problem_single_shot import Single_shot_definition
from .nmpc_problem_multiple_shot import Multiple_shot_definition

class Nmpc_panoc:
    """ Defines a nmpc problem of the shape min f(x)+ g(x) """
    def __init__(self, location_lib,model,stage_cost):
        self._location_lib=location_lib # location of the library
        self._model=model
        self._dimension_panoc=0 # dimension of the panoc problem, should be set so something non-zero

        self._stage_cost=stage_cost

        self._horizon=10
        self._shooting_mode="single shot"

        self._lbgfs_buffer_size=20
        self._data_type = "double precision"

        self._panoc_max_steps=20
        self._panoc_min_steps=10
        self._min_residual=-5 #chose 10^{-5} as max residual#

        self._integrator_casadi=False

        # generate the dynamic_globals file
        self._globals_generator = Globals_generator(self._location_lib + "globals/globals_dyn.h")

        # at first assume no obstacles
        self._obstacle=[]

    def generate_code(self):
        """ Generate code controller """
        # start with generating the cost function
        if(self._shooting_mode=='single shot'):
            self.__generate_cost_function_singleshot()
        elif(self._shooting_mode=='multiple shot'):
            self.__generate_cost_function_multipleshot()
        else:
            print('ERROR in generating code: invalid choice of shooting mode [single shot|multiple shot]')

        self._globals_generator.generate_globals(self)

        # optional feature, a c version of the integrator
        if(self._integrator_casadi):
            self.__generate_integrator()

        self._model.generate_constraint(self._location_lib)

    def __generate_integrator(self):
        """ private function, generates an integrator of the system, usefull for debugging """
        state = cd.SX.sym('istate', self._model.number_of_states, 1)
        input = cd.SX.sym('input', self._model.number_of_inputs , 1)

        integrator = cd.Function('integrator', [state, input], [self._model.get_next_state(state,input)])
        ccg.translate_casadi_to_c(integrator,self._location_lib, filename="integrator.c")

    def __generate_cost_function_singleshot(self):
        """ private function, generates part of the casadi cost function with single shot """
        ssd = Single_shot_definition(self)
        (self._cost_function, self._cost_function_derivative_combined) = ssd.generate_cost_function()
        self._dimension_panoc=ssd.dimension

    def __generate_cost_function_multipleshot(self):
        """ private function, generates part of the casadi cost function with multiple shot """
        msd = Multiple_shot_definition(self)
        (self._cost_function, self._cost_function_derivative_combined) = msd.generate_cost_function()
        self._dimension_panoc = msd.dimension

    def stage_cost(self,current_state,input,i,state_reference,input_reference):
        return self._stage_cost.stage_cost(current_state,input,i,state_reference,input_reference)
    def generate_cost_obstacles(self,state,obstacle_weights):
        if(self.number_of_obstacles==0):
            return 0.
        else:
            cost = 0.
            for i in range(0,self.number_of_obstacles):
                cost += obstacle_weights[i]*self._obstacle[i].evaluate_cost(state[self._model.indices_coordinates])

            return cost
    def add_obstacle(self,obstacle):
        self._obstacle.append(obstacle)
    @property
    def number_of_obstacles(self):
        return len(self._obstacle)
    @property
    def shooting_mode(self):
        return self._shooting_mode
    @shooting_mode.setter
    def shooting_mode(self, value):
        self._shooting_mode = value

    @property
    def dimension_panoc(self):
        return self._dimension_panoc

    @property
    def horizon(self):
        return self._horizon
    @horizon.setter
    def horizon(self, value):
        self._horizon = value

    @property
    def model(self):
        return self._model
    @model.setter
    def model(self, value):
        self._model = value

    @property
    def lbgfs_buffer_size(self):
        return self._lbgfs_buffer_size
    @lbgfs_buffer_size.setter
    def lbgfs_buffer_size(self, value):
        self._lbgfs_buffer_size = value

    @property
    def data_type(self):
        return self._data_type
    @data_type.setter
    def data_type(self, value):
        self._data_type = value

    @property
    def panoc_max_steps(self):
        return self._panoc_max_steps
    @panoc_max_steps.setter
    def panoc_max_steps(self, value):
        self._panoc_max_steps = value

    @property
    def integrator_casadi(self):
        return self._integrator_casadi
    @integrator_casadi.setter
    def integrator_casadi(self, value):
        self._integrator_casadi = value

    @property
    def location(self):
        return self._location_lib
    @location.setter
    def location(self, value):
        self._location_lib = value
        
    @property
    def panoc_min_steps(self):
        return self._panoc_min_steps
    @panoc_min_steps.setter
    def panoc_min_steps(self, value):
        self._panoc_min_steps = value
    
    @property
    def min_residual(self):
        return self._min_residual
    @min_residual.setter
    def min_residual(self, value):
        self._min_residual = value

    @property
    def number_of_obstacles(self):
        return len(self._obstacle)

    @property
    def cost_function(self):
        return self._cost_function
    @property
    def cost_function_derivative_combined(self):
        return self._cost_function_derivative_combined

