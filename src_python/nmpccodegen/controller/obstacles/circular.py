from .obstacle import  Obstacle
import casadi as cd
import matplotlib as plt
import numpy as np

class Circular(Obstacle):
    def __init__(self,model,center_coordinates,radius):
        """ construct obstable of form a[i,:]^Tb +b , for all i """
        super(Circular, self).__init__(model)

        self._center_coordinates=center_coordinates
        self._radius=radius

    def evaluate_coordinate_state_cost(self,coordinates_state):
        """ check how far coordinates are from center, if inside radius punish """
        return Obstacle.trim_and_square(self._radius - cd.sqrt(cd.sum1((self._center_coordinates-coordinates_state)**2)))

    def plot(self):
        circle = plt.patches.Circle((self._center_coordinates[0],self._center_coordinates[1]),radius=self._radius,fill=False)
        ax = plt.pyplot.gca()
        ax.add_patch(circle)

    @property
    def radius(self):
        return self._radius
    @property
    def center_coordinates(self):
        return self._center_coordinates