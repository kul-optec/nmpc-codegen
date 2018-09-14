from .obstacle import  Obstacle
import casadi as cd

class Nonconvex_constraints(Obstacle):
    def __init__(self,model):
        """ construct obstacle """
        super(Nonconvex_constraints, self).__init__(model)
        self._constraints=[]
    def add_constraint(self,constraint):
        self._constraints.append(constraint)
    def evaluate_coordinate_state_cost(self,coordinates_state):
        """ evaluate the function h(x) """
        if self.number_of_constraints == 0:
            return 0
        # if there actually are constraints:
        value=1.
        for i in range(0,self.number_of_constraints):
            h = self._constraints[i]
            value *= Obstacle.trim_and_square( \
                h(coordinates_state)\
                )
        return value

    @property
    def number_of_constraints(self):
        return len(self._constraints)