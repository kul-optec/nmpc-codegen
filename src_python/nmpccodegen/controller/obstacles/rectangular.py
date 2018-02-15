from .obstacle import  Obstacle
from .polyhedral import Obstacle_polyhedral
import casadi as cd
import matplotlib as plt
import numpy as np

class Obstacle_rectangular(Obstacle):
    def __init__(self,center_coordinates,width,height):
        """ construct obstable of form a[i,:]^Tb +b , for all i """
        self._center_coordinates=center_coordinates
        self._width = width
        self._height = height

    def evaluate_cost(self,coordinates_state):
        x_up = self._center_coordinates[0] + self._width / 2
        x_down = self._center_coordinates[0] - self._width / 2
        y_up = self._center_coordinates[1] + self._height / 2
        y_down = self._center_coordinates[1] - self._height / 2

        a = np.matrix([[-1., 0.], [1., 0.], [0., -1.], [0., 1.]]).T
        b = np.array([x_up, -x_down, y_up, -y_down])
        return Obstacle_polyhedral(a, b).evaluate_cost(coordinates_state)
    def plot(self):
        rectangular = plt.patches.Rectangle((self._center_coordinates[0]- self._width / 2,self._center_coordinates[1]- self._height / 2),self._width,self._height,fill=False)
        ax = plt.pyplot.gca()
        ax.add_patch(rectangular)

    @property
    def width(self):
        return self._width
    @property
    def height(self):
        return self._height
    @property
    def center_coordinates(self):
        return self._center_coordinates