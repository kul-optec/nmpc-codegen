from .obstacle import  Obstacle
import casadi as cd

class Obstacle_nonconvex_constraints(Obstacle):
    def __init__(self):
        """ construct obstacle """
        self._constraints=[]
    def add_constraint(self,constraint):
        self._constraints.append(constraint)
    def evaluate_cost(self,coordinates_state):
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