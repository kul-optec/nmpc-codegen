class Constraint:
    """ A interface that represents the minimum interface of an
            general constraint
        A constraint needs at least the following method:
                - evaluate_cost , evaluates the cost of the constraint """
    def evaluate_cost(self,state,input):
        raise NotImplementedError