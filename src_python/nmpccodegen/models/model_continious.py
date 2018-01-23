from . import model as m
from . import integrators as ig
import numpy as np

class Model_continious(m.Model):
    def __init__(self,system_equations,g,step_size,number_of_states,number_of_inputs,coordinates_indices,integrator):
        super(Model_continious,self).__init__(system_equations,g,step_size,number_of_states,number_of_inputs,coordinates_indices)
        self._integrator=integrator

    def get_next_state(self,state,input):
        """ integrate the continous system with one step using the selected integrator """
        system_equation = lambda state: super(Model_continious, self).system_equations(state, input)
        return ig.integrator_RK_lib(state, super(Model_continious,self).step_size, system_equation,self._integrator)
        # if (self._integrator == "RK"):
        #     system_equation = lambda state: super(Model_continious,self).system_equations(state, input)
        #     return ig.integrator_RK(state, super(Model_continious,self).step_size, system_equation)
        # else:
        #     raise NotImplementedError
    def get_next_state_numpy(self,state,input):
        number_of_state=super(Model_continious,self).number_of_states
        new_state=np.zeros((number_of_state,1))

        state_casadi = self.get_next_state(state,input)
        for j in range(0, number_of_state):
            new_state[j] = float(state_casadi[j])
        return new_state

    @property
    def integrator(self):
        return self._integrator
    @integrator.setter
    def integrator(self, value):
        self._integrator = value