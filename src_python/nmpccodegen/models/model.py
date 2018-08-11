class Model:
    """ 
    A discrete model describing the system behavior
       - If your model is continuous use the Model_continuous class. 
    """
    def __init__(self,system_equations,input_constraint,step_size,number_of_states,number_of_inputs,indices_coordinates):
        """
        Constructor Model

        Parameters
        ---------
        system_equations : The discrete system equations, expressed as Patlab functions in the form f(state,input).
        input_constraint : The input constraints, must be a nmpccodegen.Cfunctions.ProximalFunction object.
        step_size : The step size of the discrete system.
        number_of_states : The dimension of the state.
        number_of_inputs : The dimension of the input.
        indices_coordinates : indices of the states determining the location of an object

        Returns
        ------
        Nothing
        """
        self._system_equations=system_equations
        self._input_constraint=input_constraint
        self._step_size=step_size
        self._number_of_states=number_of_states
        self._number_of_inputs=number_of_inputs
        self._indices_coordinates=indices_coordinates

    def get_next_state(self,state,input):
        """ 
        Obtain the next state of the discrete system 

        Parameters
        ---------
        state -- the current state of the system
        input -- the current input of the system

        Returns
        ------
        Python array containing the next state
        """
        return self._system_equations(state,input)

    def generate_constraint(self,location):
        """
        Generate constraints in C code.

        Parameters
        ---------
        location: target location of code generator

        """
        self._input_constraint.generate_c_code(location+"/casadi/g.c")
        self._input_constraint.prox.generate_c_code(location + "/casadi/proxg.c")

    @property
    def system_equations(self):
        """
        Get or set the discrete system equations, expressed as Python functions in the form f(state,input).
        """
        return self._system_equations

    @property
    def step_size(self):
        """
        Get or set the system equations, expressed as Python functions in the form f(state,input).
        """
        return self._step_size
    @step_size.setter
    def step_size(self, value):
        self._step_size = value

    @property
    def number_of_states(self):
        """
        Get or set The dimension of the state.
        """
        return self._number_of_states
    @number_of_states.setter
    def numer_of_states(self, value):
        self._number_of_states = value

    @property
    def number_of_inputs(self):
        """
        Get or set The dimension of the input.
        """
        return self._number_of_inputs
    @number_of_inputs.setter
    def numer_of_inputs(self, value):
        self._number_of_inputs = value

    @property
    def indices_coordinates(self):
        """
        Get or set indices of the states determining the location of an object
        """
        return self._indices_coordinates
    @indices_coordinates.setter
    def indices_coordinates(self, value):
        self._indices_coordinates = value