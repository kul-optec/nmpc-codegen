class Stage_cost_QR:
    """ Simple QR stage cost"""
    def __init__(self,model,Q,R):
        self._Q=Q
        self._R=R
        self._model=model
    def evaluate_cost(self,state,input,iteration_index,
        state_reference,input_reference):
        """ calculate and return stage cost """
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