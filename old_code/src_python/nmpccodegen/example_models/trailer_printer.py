import numpy as np
import matplotlib.pyplot as plt
import math

def trailer_print(trailer_states,color="k"):
    """ print out the states of a trailer """
    # trailer_states = np array of shape (number_of_states,number_of_steps)
    (number_of_states, number_of_steps) = np.shape(trailer_states)
    size=0.01

    for i in range(0,number_of_steps):
        x = trailer_states[0,i]
        y = trailer_states[1, i]
        dx = math.cos(trailer_states[2, i])*size
        dy = math.sin(trailer_states[2, i])*size

        plt.arrow(x, y, dx, dy, fc=color, ec=color, head_width=0.005, head_length=0.01)

def draw_rectangular_obstacle(x_up,x_down,y_up,y_down):
    """ print an obstacle """
    plt.plot([x_down,x_up,x_up,x_down,x_down,],[y_up,y_up,y_down,y_down,y_up])
def draw_rectangular_obstacle_around_center(center_coordinates,width,height):
    x_up = center_coordinates[0] + width / 2
    x_down = center_coordinates[0] - width / 2
    y_up = center_coordinates[1] + height / 2
    y_down = center_coordinates[1] - height / 2
    return draw_rectangular_obstacle(x_up, x_down, y_up, y_down)

if __name__ == '__main__':
    example = np.array([[0,0,math.pi/4],[0.5,0.5,math.pi/2]])

    plt.figure(0)
    trailer_print(example.T,[0, 1],[0, 1])