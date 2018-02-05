import casadi as cd
import numpy as np

class Obstacle:
    def evaluate_cost(self,coordinates_state):
        """ evaluate the function h(x) """
        raise NotImplementedError
    @staticmethod
    def trim_and_square(x):
        return  cd.fmax(x,0)**2