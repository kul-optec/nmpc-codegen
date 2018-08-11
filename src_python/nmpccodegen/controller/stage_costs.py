class Stage_cost_QR:
    """ 
    Simple QR stage cost
    """
    def __init__(self,model,Q,R):
        """
        Constructs stage cost

        Parameters
        ---------
        model : object of nmpccodegen.models.model or nmpccodegen.models.model_continious 
        Q : quadratic cost on the state
        R : quadratic cost on the input
        """
        self._Q=Q
        self._R=R
        self._model=model
    def evaluate_cost(self,state,input,iteration_index,
        state_reference,input_reference):
        """ 
        Calculate stage cost 

        Parameters
        ---------
        state : current state of the system
        input : current input of the system
        iteration_index : step index of the discrete system
        state_reference : wanted state of the system
        input_reference : wanted input of the system

        Returns
        ------
        Stage Cost (x'Qx + u'Ru)
        """
        # As state and input are of the stype csadi.SX we can't just do vector matrix product
        # Everything must be written out in basic operations
        stage_cost=0

        for i_col in range(0,self._model.number_of_states):
            for i_row in range(0, self._model.number_of_states):
                stage_cost += (state[i_col]-state_reference[i_col])*\
                            self._Q[i_col,i_row]*\
                            (state[i_row]-state_reference[i_row])

        for i_col in range(0,self._model.number_of_inputs):
            for i_row in range(0, self._model.number_of_inputs):
                stage_cost += (input[i_col]-input_reference[i_col])*\
                            self._R[i_col,i_row]*\
                            (input[i_row]-input_reference[i_row])

        return stage_cost