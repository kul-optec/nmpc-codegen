import casadi as cd

class Input_norm:
    """ Constraint that punishes if the 2-norm of the input is too high """
    def __init__(self,max_norm):
        self._max_norm=max_norm

    def evaluate_cost(self,state,input):
        norm_input = cd.sum1(input**2)
        cost = cd.fmax(norm_input - self._max_norm ** 2, 0) ** 2

        return cost