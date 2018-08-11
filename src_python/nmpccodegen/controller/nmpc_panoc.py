import casadi as cd
import numpy as np
import os
from pathlib import Path

from .globals_generator import Globals_generator
from .casadi_code_generator import Casadi_code_generator as ccg
from .nmpc_problem_single_shot import Single_shot_definition
from .nmpc_problem_single_shot_LA import Single_shot_LA_definition
from .nmpc_problem_multiple_shot import Multiple_shot_definition

class Nmpc_panoc:
    """ 
    A nmpc problem of the shape min f(x)+ g(x) 
    """
    def __init__(self, location_lib,model,stage_cost,terminal_cost=None):
        """
        Constructors a controller

        Parameters
        ---------
        location_lib : Location of the folder in which the control should be generated.
        model : The discrete or continues model.
        stage_cost : The stage cost object
        terminal_cost : The optional terminal cost of object, if no
        terminal costs is provided than the stage cost will be used as terminal cost.
        """
        self._location_lib=location_lib # location of the library
        self._model=model
        self._dimension_panoc=0 # dimension of the panoc problem, should be set so something non-zero

        self._stage_cost=stage_cost
        if(terminal_cost==None):
            self._terminal_cost=stage_cost
        else:
            self._terminal_cost=terminal_cost

        self._horizon=10
        self._shooting_mode="single shot"

        self._lbgfs_buffer_size=20
        self._data_type = "double precision"

        self._panoc_max_steps=20
        self._panoc_min_steps=0
        self._min_residual=-5 #chose 10^{-5} as max residual#

        self._integrator_casadi=False
        self._pure_prox_gradient=False
        self._shift_input=True

        # Accelerated Lagrangian related properties
        self._general_constraints=[]
        self._constraint_optimal_value=1e3
        self._constraint_max_weight=1e5
        self._start_residual=1
        self._max_steps_LA=4

        # generate the dynamic_globals file
        self._globals_generator = Globals_generator(self._location_lib + "/globals/globals_dyn.h")

        # at first assume no constraints
        self._constraints=[]

    def generate_code(self):
        """ 
        Generate code controller 
        """
        # start with generating the cost function
        if(self._shooting_mode=='single shot'):
            if(self.number_of_general_constraints==0):
                self.__generate_cost_function_singleshot()
            else:
                self.__generate_cost_function_singleshot_LA()
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
        """ 
        private function, generates an integrator of the system, usefull for debugging 
        """
        state = cd.SX.sym('istate', self._model.number_of_states, 1)
        input = cd.SX.sym('input', self._model.number_of_inputs , 1)

        integrator = cd.Function('integrator', [state, input], [self._model.get_next_state(state,input)])
        ccg.translate_casadi_to_c(integrator,self._location_lib, filename="integrator")

    def __generate_cost_function_singleshot(self):
        """ 
        private function, generates part of the casadi cost function with single shot 
        """
        ssd = Single_shot_definition(self)
        (self._cost_function, self._cost_function_derivative_combined) = ssd.generate_cost_function()
        self._dimension_panoc=ssd.dimension
    def __generate_cost_function_singleshot_LA(self):
        """ 
        private function, generates part of the casadi cost function with single shot, using the accelerated Lagrangian 
        """
        ssd = Single_shot_LA_definition(self)
        (self._cost_function, self._cost_function_derivative_combined) = ssd.generate_cost_function()
        self._dimension_panoc=ssd.dimension

    def __generate_cost_function_multipleshot(self):
        """ 
        private function, generates part of the casadi cost function with multiple shot 
        """
        msd = Multiple_shot_definition(self)
        (self._cost_function, self._cost_function_derivative_combined) = msd.generate_cost_function()
        self._dimension_panoc = msd.dimension

    def stage_cost(self,current_state,input,i,state_reference,input_reference):
        if(i==self._horizon-1):
            return self._terminal_cost.evaluate_cost(current_state,input,i,state_reference,input_reference)
        return self._stage_cost.evaluate_cost(current_state,input,i,state_reference,input_reference)

    def generate_cost_constraints(self,state,input,constraint_weights):
        """
        Function used internally to calculate the costs of the constraints.
        """
        if(self.number_of_constraints is 0):
            return 0.
        else:
            cost = 0.
            for i in range(0,self.number_of_constraints):
                cost += constraint_weights[i]*self._constraints[i].evaluate_cost(state,input)

            return cost

    def add_constraint(self,constraint):
        """
        Add an constraint to the controller.

        Parameters
        ---------
        constraint : a constraint
        """
        self._constraints.append(constraint)

    @property
    def number_of_constraints(self):
        """
        Get the number of added constraints
        """
        return len(self._constraints)

    def add_general_constraint(self,general_constraint):
        self._general_constraints.append(general_constraint)
    @property
    def number_of_general_constraints(self):
        """
        Get the number of added general constraints
        """
        return len(self._general_constraints)

    @property
    def shooting_mode(self):
        """
        Get or set the shooting mode, should be either "single shot" or "multiple shot"
        """
        return self._shooting_mode
    @shooting_mode.setter
    def shooting_mode(self, value):
        self._shooting_mode = value

    @property
    def dimension_panoc(self):
        """
        Get the dimension of the optimization problem after the code generation
        """
        return self._dimension_panoc

    @property
    def horizon(self):
        """
        Get or set the horizon of the controller problem.
        """
        return self._horizon
    @horizon.setter
    def horizon(self, value):
        self._horizon = value

    @property
    def shift_input(self):
        """
        Get or set if the input horizon will be shifted after returning the optimal input (true means shifting)
        """
        return self._shift_input
    @shift_input.setter
    def shift_input(self, value):
        self._shift_input = value

    @property
    def model(self):
        """
        Get or set the model of the system that the controller controls provided by the constructor.
        """
        return self._model
    @model.setter
    def model(self, value):
        self._model = value

    @property
    def lbgfs_buffer_size(self):
        """
        Get or set the buffer size of the lbfgs method.
        """
        return self._lbgfs_buffer_size
    @lbgfs_buffer_size.setter
    def lbgfs_buffer_size(self, value):
        self._lbgfs_buffer_size = value

    @property
    def data_type(self):
        """
        Get or set the required precision of the controller, should be either "single precision" or "double precision" .
        """
        return self._data_type
    @data_type.setter
    def data_type(self, value):
        self._data_type = value

    @property
    def panoc_max_steps(self):
        """
        Get or set the maximum amount of steps the panoc algorithm should take.
        """
        return self._panoc_max_steps
    @panoc_max_steps.setter
    def panoc_max_steps(self, value):
        self._panoc_max_steps = value

    @property
    def integrator_casadi(self):
        """
        Get or set whenether there needs to be a integrator generated in C (if true it will generate integrator)
        """
        return self._integrator_casadi
    @integrator_casadi.setter
    def integrator_casadi(self, value):
        self._integrator_casadi = value
    @property
    def pure_prox_gradient(self):
        """
        Get or set whenether to use the the quasi Newton method or not, if false it will use PANOC if true it will use proximal gradient
        """
        return self._pure_prox_gradient
    @pure_prox_gradient.setter
    def pure_prox_gradient(self, value):
        self._pure_prox_gradient = value

    @property
    def location(self):
        """
        Get or set the location where the control needs to be generated.
        """
        return self._location_lib
    @location.setter
    def location(self, value):
        self._location_lib = value
        
    @property
    def panoc_min_steps(self):
        """
        Get or set the minimum amount of steps the panoc algorithm should take.
        """
        return self._panoc_min_steps
    @panoc_min_steps.setter
    def panoc_min_steps(self, value):
        self._panoc_min_steps = value
    
    @property
    def min_residual(self):
        """
        Get or set the power required precision of the residual, the residual will be required to be 10^min_residual
        """
        return self._min_residual
    @min_residual.setter
    def min_residual(self, value):
        self._min_residual = value

    @property
    def constraint_optimal_value(self):
        """
        Get or set when the weighted constraint should stop increasing the weight
        """
        return self._constraint_optimal_value
    @constraint_optimal_value.setter
    def constraint_optimal_value(self, value):
        self._constraint_optimal_value = value

    @property
    def constraint_max_weight(self):
        """
        Get or set max value of the weight on the general constraints
        """
        return self._constraint_max_weight

    @constraint_max_weight.setter
    def constraint_max_weight(self, value):
        self._constraint_max_weight = value

    @property
    def start_residual(self):
        """
        Get or set the start residual of the accelerated lagrangian
        """
        return self._start_residual
    @start_residual.setter
    def start_residual(self, value):
        self._start_residual = value

    @property
    def max_steps_LA(self):
        """
        Get or set max amount of outer looops/step of the accelerated lagrangian 
        """
        return self._max_steps_LA
    @max_steps_LA.setter
    def max_steps_LA(self, value):
        self._max_steps_LA = value

    @property
    def constraints(self):
        """
        Get the constraints that where added with the add_constraint method 
        """
        return self._constraints
    @property
    def general_constraints(self):
        """
        Get the general constraints that where added with the add_general_constraint method
        """
        return self._general_constraints
    @property
    def cost_function(self):
        """
        Get the cost function and gradient of the MPC problem

        Returns
        ------
        [x] = f(x,u)
        """
        return self._cost_function
    @property
    def cost_function_derivative_combined(self):
        """
        Get the cost function and gradient of the MPC problem

        Returns
        ------
        [x,dx] = f_df(x,u)
        """
        return self._cost_function_derivative_combined

