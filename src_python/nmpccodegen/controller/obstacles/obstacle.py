import casadi as cd
import numpy as np

class Obstacle:
    def __init__(self,model):
        self._model=model

    def evaluate_cost(self,state,input):
        """ evaluate the function h(x) """
        cost = self.evaluate_coordinate_state_cost(state[self._model.indices_coordinates])
        return cost

    def evaluate_coordinate_state_cost(self,coordinates_state):
        raise NotImplementedError

    @staticmethod
    def trim_and_square(x):
        return  cd.fmax(x,0)**2

    @property
    def model(self):
        return self._model