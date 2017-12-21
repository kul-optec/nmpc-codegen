import casadi as cd
import numpy as np
import os
from pathlib import Path
import globals_generator as gg

class Nmpc_panoc:
    """ Defines a nmpc problem of the shape min f(x)+ g(x) """
    def __init__(self, location_lib,model,stage_cost):
        self._location_lib=location_lib # location of the library
        self._model=model

        self._stage_cost=stage_cost

        self._number_of_steps=10
        self._shooting_mode="single shot"

        self._lbgfs_buffer_size=10
        self._data_type = "double precision"

        self._panoc_max_steps=10

        self._integrator_casadi=False

        # generate the dynamic_globals file
        self._globals_generator = gg.Globals_generator(self._location_lib + "globals/globals_dyn.h")



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
        """ private function, generates part of the casadi cost function with single shot"""
        initial_state = cd.SX.sym('initial_state', self._model.number_of_states, 1)
        input_all_steps = cd.SX.sym('input_all_steps', self._model.number_of_inputs*self._number_of_steps, 1)

        cost=cd.SX.sym('cost',1,1)
        cost=0

        current_state=initial_state
        for i in range(1,self._number_of_steps+1):
            input = input_all_steps[(i-1)*self._model.number_of_inputs:i*self._model.number_of_inputs]
            current_state = self._model.get_next_state(current_state,input)
            cost = cost + self._stage_cost.stage_cost(current_state,input,i)

        cost = cost + self.__generate_cost_obstacles()
        self.__setup_casadi_functions_and_generate_c(initial_state,input_all_steps,cost)

    def __setup_casadi_functions_and_generate_c(self,initial_state,input_all_steps,cost):
        self._cost_function = cd.Function('cost_function', [initial_state, input_all_steps], [cost])
        self._cost_function_derivative = cd.Function('cost_function_derivative', [initial_state, input_all_steps],
                                               [cd.jacobian(cost, input_all_steps)])
        self._cost_function_derivative_combined = cd.Function('cost_function_derivative_combined',
                                                        [initial_state, input_all_steps],
                                                        [cost, cd.jacobian(cost, input_all_steps)])

        self.__translate_casadi_to_c(self._cost_function, filename="cost_function.c")
        self.__translate_casadi_to_c(self._cost_function_derivative, filename="cost_function_derivative.c")
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
    def cost_function(self):
        return self._cost_function
    @property
    def cost_function_derivative(self):
        return self._cost_function_derivative
    @property
    def cost_function_derivative_combined(self):
        return self._cost_function_derivative_combined

