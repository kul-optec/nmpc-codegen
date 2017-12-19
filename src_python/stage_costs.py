class Stage_cost_QR:
    """ Simple QR stage cost"""
    def __init__(self,model,Q,R):
        self._Q=Q
        self._R=R
        self._model=model
    def stage_cost(self,state,input,iteration_index):
        # As state and input are of the stype csadi.SX we can't just do vector matrix product
        # Everything must be written out in basic operations
        stage_cost=0
        for i_col in range(1,self._model.number_of_states):
            for i_row in range(1, self._model.number_of_states):
                stage_cost += state[i_col]*self._Q[i_col,i_row]*state[i_row]
        for i_col in range(1,self._model.number_of_inputs):
            for i_row in range(1, self._model.number_of_inputs):
                stage_cost += input[i_col]*self._R[i_col,i_row]*input[i_row]
        return stage_cost

class Stage_cost_QR_reference:
    """ Simple QR stage cost using a single state reference"""
    def __init__(self,model,Q,R,state_reference):
        self._Q=Q
        self._R=R
        self._model=model
        self._state_reference = state_reference
    def stage_cost(self,state,input,iteration_index):
        # As state and input are of the stype csadi.SX we can't just do vector matrix product
        # Everything must be written out in basic operations
        stage_cost=0
        for i_col in range(1,self._model.number_of_states):
            for i_row in range(1, self._model.number_of_states):
                stage_cost += (state[i_col]-self._state_reference[i_col])*\
                               self._Q[i_col,i_row]*\
                              (state[i_row]-self._state_reference[i_col])
        for i_col in range(1,self._model.number_of_inputs):
            for i_row in range(1, self._model.number_of_inputs):
                stage_cost += input[i_col]*self._R[i_col,i_row]*input[i_row]
        return stage_cost