from .obstacle import  Obstacle
import casadi as cd

class Polyhedral(Obstacle):
    def __init__(self,model,a,b):
        """ construct obstacle of form a[i,:]^Tb +b , for all i """
        super(Polyhedral, self).__init__(model)

        self._a=a
        self._b=b

        (dimension,number_of_constraints) = a.shape

        self._number_of_constraints=number_of_constraints
        self._dimension=dimension

    def evaluate_coordinate_state_cost(self,coordinates_state):
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