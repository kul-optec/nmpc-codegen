class Model:
    """ NMPC discrete model """
    def __init__(self,system_equations,input_constraint,step_size,number_of_states,number_of_inputs,indices_coordinates):
        self._system_equations=system_equations
        self._input_constraint=input_constraint
        self._step_size=step_size
        self._number_of_states=number_of_states
        self._number_of_inputs=number_of_inputs
        self._indices_coordinates=indices_coordinates

    def get_next_state(self,state,input):
        return self._system_equations(state,input)

    def generate_constraint(self,location):
        self._input_constraint.generate_c_code(location+"/casadi/g.c")
        self._input_constraint.prox.generate_c_code(location + "/casadi/proxg.c")

    @property
    def system_equations(self):
        return self._system_equations

    @property
    def step_size(self):
        return self._step_size
    @step_size.setter
    def step_size(self, value):
        self._step_size = value

    @property
    def number_of_states(self):
        return self._number_of_states
    @number_of_states.setter
    def numer_of_states(self, value):
        self._number_of_states = value

    @property
    def number_of_inputs(self):
        return self._number_of_inputs
    @number_of_inputs.setter
    def numer_of_inputs(self, value):
        self._number_of_inputs = value

    @property
    def indices_coordinates(self):
        return self._indices_coordinates
    @indices_coordinates.setter
    def indices_coordinates(self, value):
        self._indices_coordinates = value