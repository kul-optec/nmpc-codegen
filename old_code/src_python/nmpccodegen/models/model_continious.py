from . import model as m
from . import integrators as ig
import numpy as np

class Model_continious(m.Model):
    """"
    A contious model describing the system behavior
       - The same as a model, but the user provides a continue model and
       the name of an integrator to discretize it
    """
    def __init__(self,system_equations,g,step_size,number_of_states,number_of_inputs,coordinates_indices,integrator):
        """
        Constructor Model

        Parameters
        ---------
        system_equations : The continue system equations, expressed as Patlab functions in the form f(state,input).
        input_constraint : The input constraints, must be a nmpccodegen.Cfunctions.ProximalFunction object.
        step_size : The step size of the discrete system.
        number_of_states : The dimension of the state.
        number_of_inputs : The dimension of the input.
        indices_coordinates : indices of the states determining the location of an object
        integrator : integrator name (for example "FE" or "RK44")

        Returns
        ------
        Nothing
        """
        super(Model_continious,self).__init__(system_equations,g,step_size,number_of_states,number_of_inputs,coordinates_indices)
        self._integrator=integrator

    def get_next_state(self,state,input):
        """ 
        Obtain the next state of the discrete system 

        Parameters
        ---------
        state -- the current state of the system
        input -- the current input of the system

        Returns
        ------
        Casadi array containing the next state 
        """
        system_equation = lambda state: super(Model_continious, self).system_equations(state, input)
        return ig.integrator_RK_lib(state, super(Model_continious,self).step_size, system_equation,self._integrator)

    def get_next_state_numpy(self,state,input):
        """ 
        Obtain the next state of the discrete system 

        Parameters
        ---------
        state -- the current state of the system
        input -- the current input of the system

        Returns
        ------
        Numpy array containing the next state 
        """
        number_of_state=super(Model_continious,self).number_of_states
        new_state=np.zeros((number_of_state,1))

        state_casadi = self.get_next_state(state,input)
        for j in range(0, number_of_state):
            new_state[j] = float(state_casadi[j])
        return new_state

    @property
    def integrator(self):
        """
        Get or set the integrator keyname
        """
        return self._integrator
    @integrator.setter
    def integrator(self, value):
        self._integrator = value