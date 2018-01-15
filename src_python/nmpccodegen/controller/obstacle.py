import casadi as cd
import numpy as np

class Obstacle:
    def evaluate_cost(self,coordinates_state):
        """ evaluate the function h(x) """
        raise NotImplementedError
    def trim_and_square(self,x):
        return  cd.fmax(x,0)**2

class Obstacle_polyhedral(Obstacle):
    def __init__(self,a,b):
        """ construct obstable of form a[i,:]^Tb +b , for all i """
        self._a=a
        self._b=b

        (dimension,number_of_constraints) = a.shape

        self._number_of_constraints=number_of_constraints
        self._dimension=dimension

    def evaluate_cost(self,coordinates_state):
        """ evaluate the function h(x) """
        value=1.
        for i in range(0,self._number_of_constraints):
            value *= Obstacle.trim_and_square(self,\
                cd.dot(self._a[:,i], coordinates_state) + self._b[i]\
                )

        return value

    @property
    def number_of_constraints(self):
        return self._number_of_constraints

class Basic_obstacles:
    def generate_rec_object(x_up, x_down, y_up, y_down):
        a = np.matrix([[-1., 0.], [1., 0.], [0., -1.], [0., 1.]]).T
        b = np.array([x_up, -x_down, y_up, -y_down])
        return Obstacle_polyhedral(a, b)