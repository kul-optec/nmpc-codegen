# library containing tools to convert system dynamics into an optimal control problem

class Chain_dyn_optimal_control_parameters:
    """ optimal control parameters """
    def __init__(self,beta,gamma,delta,x_ref):
        self.beta=beta
        self.gamma=gamma
        self.delta=delta
        self.x_ref=x_ref