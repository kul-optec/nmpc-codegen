import casadi as cd
import numpy as np
import os
from pathlib import Path
import globals_generator as gg

class Nmpc_panoc:
    """ Defines a nmpc problem of the shape min f(x)+ g(x) """
    def __init__(self, location_lib,model,Q,R):
        self._location_lib=location_lib # location of the library
        self._model=model

        self._Q=Q
        self._R = R

        self._number_of_steps=10
        self._shooting_mode="single shot"

        self._lbgfs_buffer_size=10
        self._data_type = "double precision"

        # generate the dynamic_globals file
        self._globals_generator = gg.Globals_generator(self._location_lib + "globals/globals_dyn.h")

    def stage_cost(self,state,input):
        # As state and input are of the stype csadi.SX we can't just do vector matrix product
        # Everything must be written out in basic operations
        stage_cost=0
        for i_col in range(1,self._model.number_of_states):
            for i_row in range(1, self._model.number_of_states):
                stage_cost += state[i_col]*self._Q[i_col,i_row]*state[i_row]
        for i_col in range(1,self._model.number_of_inputs):
            for i_row in range(1, self._model.number_of_inputs):
                stage_cost += input[i_col]*self._R[i_col,i_row]*input[i_row]
        return stage_cost

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

    def __generate_cost_function_singleshot(self):
        """ private function, generates part of the casadi cost function with single shot"""
        initial_state = cd.SX.sym('initial_state', self._model.number_of_states, 1)
        input_all_steps = cd.SX.sym('input_all_steps', self._model.number_of_inputs*self._number_of_steps, 1)

        cost=cd.SX.sym('cost',1,1)
        cost=0

        current_state=initial_state
        for i in range(1,self._number_of_steps):
            input = input_all_steps[(i-1)*self._model.number_of_inputs:i*self._model.number_of_inputs]
            current_state = self._model.get_next_state(current_state,input)
            cost = cost + self.stage_cost(current_state,input)

        cost = cost + self.__generate_cost_obstacles()
        self.__setup_casadi_functions_and_generate_c(initial_state,input_all_steps,cost)

    def __setup_casadi_functions_and_generate_c(self,initial_state,input_all_steps,cost):
        cost_function = cd.Function('cost_function', [initial_state, input_all_steps], [cost])
        cost_function_derivative = cd.Function('cost_function_derivative', [initial_state, input_all_steps],
                                               [cd.jacobian(cost, initial_state)])
        cost_function_derivative_combined = cd.Function('cost_function_derivative_combined',
                                                        [initial_state, input_all_steps],
                                                        [cost, cd.jacobian(cost, initial_state)])

        self.__translate_casadi_to_c(cost_function, filename="cost.c")
        self.__translate_casadi_to_c(cost_function_derivative, filename="cost_derivative.c")
        self.__translate_casadi_to_c(cost_function_derivative_combined, filename="cost_derivative_combined.c")
    def __translate_casadi_to_c(self,casadi_function,filename):
        # check if the buffer file excists, should never be the case, but check anyway
        buffer_file_name="buffer"
        file = Path(buffer_file_name)
        if (file.exists()):
            os.remove(buffer_file_name)

        # generate the casadi function in C to a buffer file
        casadi_function.generate(buffer_file_name)
        file_name_costfunction = self._location_lib + "casadi/"+filename

        # check if the file already exists
        file = Path(file_name_costfunction)
        if(file.exists()):
            print(file_name_costfunction+ " already exists: removing file...")
            os.remove(file_name_costfunction)

        # move the function to the right location
        os.rename('buffer.c',file_name_costfunction)

    def __generate_cost_function_multipleshot(self,location):
        """ private function, generates part of the casadi cost function with multiple shot"""
        raise NotImplementedError
    def __generate_cost_obstacles(self):
        return 0 # TODO implementation obstacles
    def simulation(self):
        """ Simulate the controller """
        self.generate_code()
        # TODO call the make file and silumate the controller using a simulation set, return a simulation object
        raise NotImplementedError
    def generate_minimum_lib(self,location,replace):
        """ Generate a lib with minimum amount of files  """
        file = Path(location)
        if (file.exists()):
            print(location + " already exists")
            if replace==True:
                os.remove(location)
                # TODO copy over all the necessary files !
            else:
                print("ERROR folder lib already excist, remove the folder or put repace on true")

    @property
    def shooting_mode(self):
        return self._shooting_mode
    @shooting_mode.setter
    def shooting_mode(self, value):
        self._shooting_mode = value

    @property
    def number_of_steps(self):
        return self._number_of_steps
    @number_of_steps.setter
    def number_of_steps(self, value):
        self._number_of_steps = value

    @property
    def mode(self):
        return self._mode
    @mode.setter
    def mode(self, value):
        self._mode = value

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