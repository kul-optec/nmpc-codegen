class Model:
    """ NMPC discrete model """
    def __init__(self,system_equations,g,step_size):
        self._system_equations=system_equations
        self._g=g
        self._step_size=step_size

    def get_next_state(self,state,input):
        return self._system_equations(state,input)

    def generate_constraint(self,location):
        self._g.generate_code(location)

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
    def numer_of_states(self):
        return self._numer_of_states
    @numer_of_states.setter
    def numer_of_states(self, value):
        self._numer_of_states = value

    @property
    def numer_of_inputs(self):
        return self._numer_of_inputs
    @numer_of_inputs.setter
    def numer_of_inputs(self, value):
        self._numer_of_inputs = value