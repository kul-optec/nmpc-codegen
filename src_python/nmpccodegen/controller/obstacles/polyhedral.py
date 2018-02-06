from .obstacle import  Obstacle
import casadi as cd

class Obstacle_polyhedral(Obstacle):
    def __init__(self,a,b):
        """ construct obstacle of form a[i,:]^Tb +b , for all i """
        self._a=a
        self._b=b

        (dimension,number_of_constraints) = a.shape

        self._number_of_constraints=number_of_constraints
        self._dimension=dimension

    def evaluate_cost(self,coordinates_state):
        """ evaluate the function h(x) """
        value=1.
        for i in range(0,self._number_of_constraints):
            value *= Obstacle.trim_and_square(\
                cd.dot(self._a[:,i], coordinates_state) + self._b[i]\
                )

        return value

    @property
    def number_of_constraints(self):
        return self._number_of_constraints