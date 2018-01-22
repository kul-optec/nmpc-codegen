import casadi as cd
import numpy as np
import os
from pathlib import Path
from .globals_generator import Globals_generator

class Nmpc_panoc:
    """ Defines a nmpc problem of the shape min f(x)+ g(x) """
    def __init__(self, location_lib,model,stage_cost):
        self._location_lib=location_lib # location of the library
        self._model=model

        self._stage_cost=stage_cost

        self._horizon=10
        self._shooting_mode="single shot"

        self._lbgfs_buffer_size=10
        self._data_type = "double precision"

        self._panoc_max_steps=20
        self._panoc_min_steps=10
        self._min_residual=-5 #chose 10^{-5} as max residual#

        self._integrator_casadi=False

        # generate the dynamic_globals file
        self._globals_generator = Globals_generator(self._location_lib + "globals/globals_dyn.h")

        # at first assume no obstacles
        self._obstacle=[]
        self._obstacle_weights = []

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
        state = cd.SX.sym('istate', self._model.number_of_states, 1)
        input = cd.SX.sym('input', self._model.number_of_inputs , 1)

        integrator = cd.Function('integrator', [state, input], [self._model.get_next_state(state,input)])

        self.__translate_casadi_to_c(integrator, filename="integrator.c")

    def __generate_cost_function_singleshot(self):
        """ private function, generates part of the casadi cost function with single shot """
        initial_state = cd.SX.sym('initial_state', self._model.number_of_states, 1)
        state_reference = cd.SX.sym('state_reference', self._model.number_of_states, 1)
        input_reference = cd.SX.sym('input_reference', self._model.number_of_inputs, 1)

        input_all_steps = cd.SX.sym('input_all_steps', self._model.number_of_inputs*self._horizon, 1)
        cost=cd.SX.sym('cost',1,1)
        cost=0

        current_state=initial_state
        for i in range(1,self._horizon+1):
            input = input_all_steps[(i-1)*self._model.number_of_inputs:i*self._model.number_of_inputs]
            current_state = self._model.get_next_state(current_state,input)

            cost = cost + self._stage_cost.stage_cost(current_state,input,i,state_reference,input_reference)
            cost = cost + self.__generate_cost_obstacles(current_state)

        self.__setup_casadi_functions_and_generate_c(initial_state,input_all_steps,state_reference,input_reference,cost)

    def __setup_casadi_functions_and_generate_c(self,initial_state,input_all_steps,
                                                state_reference,input_reference,cost):
        self._cost_function = cd.Function('cost_function', [initial_state, input_all_steps,state_reference,input_reference], [cost])
        self._cost_function_derivative_combined = cd.Function('cost_function_derivative_combined',
                                                        [initial_state, input_all_steps,state_reference,input_reference],
                                                        [cost, cd.gradient(cost, input_all_steps)])

        self.__translate_casadi_to_c(self._cost_function, filename="cost_function.c")
        self.__translate_casadi_to_c(self._cost_function_derivative_combined, filename="cost_function_derivative_combined.c")
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
        open(file_name_costfunction, 'a').close()

        prototype_function = "(const real_t** arg, real_t** res, int* iw, real_t* w, int mem) {"
        self.__copy_over_function_to_file("buffer.c",file_name_costfunction,prototype_function)

        prototype_function = "(int *sz_arg, int* sz_res, int *sz_iw, int *sz_w) {"
        self.__copy_over_function_to_file("buffer.c", file_name_costfunction, prototype_function)

        os.remove("buffer.c")
    def __copy_over_function_to_file(self,source,destination,function_name):
        in_file=False
        destination_file = open(destination, 'a')
        with open(source, 'r') as inF:
            for line in inF:
                if function_name in line:
                    in_file=True
                if in_file:
                    destination_file.write(line)
                if "}" in line:
                    in_file = False

    def __generate_cost_function_multipleshot(self,location):
        """ private function, generates part of the casadi cost function with multiple shot"""
        raise NotImplementedError
    def __generate_cost_obstacles(self,state):
        number_of_obstacles=len(self._obstacle)
        if(number_of_obstacles==0):
            return 0.
        else:
            cost = 0.
            for i in range(0,number_of_obstacles):
                cost += self._obstacle_weights[i]*self._obstacle[i].evaluate_cost(state[self._model.indices_coordinates])

            return cost
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

    def add_obstacle(self,obstacle,weight):
        self._obstacle.append(obstacle)
        self._obstacle_weights.append(weight)
    @property
    def shooting_mode(self):
        return self._shooting_mode
    @shooting_mode.setter
    def shooting_mode(self, value):
        self._shooting_mode = value

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
    def cost_function(self):
        return self._cost_function
    @property
    def cost_function_derivative(self):
        return self._cost_function_derivative
    @property
    def cost_function_derivative_combined(self):
        return self._cost_function_derivative_combined

