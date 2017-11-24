import casadi as cd
import numpy as np
import integrators as ig

class Nmpc_panoc:
    """ Defines a nmpc problem of the shape min f(x)+ g(x) """
    def __init__(self, location_lib,f,g,d,dimension_x,dimension_u):
        self._location_lib=location_lib # location of the library
        self._g = g
        self._f = f
        self._d=d
        self._dimension_x=dimension_x
        self._dimension_u=dimension_u

        self._shooting_mode='single shot' # default=single shot, other options are: multiple shot
        self._number_of_steps=10
        self._step_size=0.1
        self._mode="continue"
        self._integrator="RK"

        self._lbgfs_buffer_size=10
        self._data_type = "double precision"

    def generate_code(self,location):
        """ Generate code controller """
        # start with generating the cost function
        if(self._shooting_mode=='single shot'):
            self.__generate_cost_function_singleshot(location)
        elif(self._shooting_mode=='multiple shot'):
            self.__generate_cost_function_multipleshot(location)
        else:
            print('ERROR in generating code: invalid choice of shooting mode [single shot|multiple shot]')

        # generate the dynamic_globals file
        raise NotImplementedError
    def __generate_cost_function_singleshot(self,location):
        """ private function, generates the casadi cost function with single shot"""
        initial_state = cd.SX.sym('initial_state', self._dimension_x, 1)
        input_all_steps = cd.SX.sym('input_all_steps', self._dimension_u*self._number_of_steps, 1)

        cost=0

        current_state=initial_state
        for i in range(1,self._number_of_steps):
            input = input_all_steps[(i-1)*self._dimension_u:i*self._dimension_u]
            current_state = self.integrate_step(current_state,input)
            cost += self._d(current_state,i)

        # TODO add obsticles

        cost_function = cd.Function('cost_function', [initial_state, input_all_steps], [cost,cd.jacobian(cost,initial_state)])
        # TODO generate C code

        cost_function.generate(location)

    def __generate_cost_function_multipleshot(self,location):
        """ private function, generates the casadi cost function with multiple shot"""
        raise NotImplementedError
    def simulation(self):
        """ Simulate the controller """
        self.generate_code()
        # TODO call the make file and silumate the controller using a simulation set, return a simulation object
        raise NotImplementedError
    def generate_minimum_lib(self,location):
        """ Generate a lib with minimum amount of files  """
        raise NotImplementedError
    def integrate_step(self,state,input):
        """ integrate one step with the selected integrator """
        if(self._integrator=="RK"):
            system_equation = lambda state: self._f(state,input)
            return ig.integrator_RK(state,self._step_size,system_equation)
        else:
            raise NotImplementedError


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
    def steps_size(self):
        return self._steps_size
    @steps_size.setter
    def steps_size(self, value):
        self._steps_size = value

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