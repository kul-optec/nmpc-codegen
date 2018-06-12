import sys
sys.path.insert(0, '../../src_python')
import nmpccodegen as nmpc
import nmpccodegen.tools as tools
import nmpccodegen.models as models
import nmpccodegen.controller as controller
import nmpccodegen.controller.obstacles as obstacles
import nmpccodegen.Cfunctions as cfunctions
import nmpccodegen.example_models as example_models

import numpy as np
import matplotlib.pyplot as plt
import math

from demo import prepare_demo_trailer,simulate_demo

if __name__ == '__main__':
    step_size=0.05

    # Q and R matrixes determined by the control engineer.
    Q = np.diag([1., 1., 0.01])*0.2
    R = np.diag([1., 1.]) * 0.01

    trailer_controller = prepare_demo_trailer(step_size,Q,R)

    trailer_controller.horizon = 30 # NMPC parameter
    trailer_controller.integrator_casadi = True # optional  feature that can generate the integrating used  in the cost function
    trailer_controller.panoc_max_steps = 500 # the maximum amount of iterations the PANOC algorithm is allowed to do.
    trailer_controller.min_residual=-3

    # construct lower rectangular
    rectangular_center_coordinates = np.array([0.45,-0.1])
    rectangular_width = 0.4
    rectangular_height = 0.1
    rectangular = obstacles.Rectangular(trailer_controller.model,rectangular_center_coordinates,\
                                                 rectangular_width,rectangular_height)

    # construct left circle
    left_circle = obstacles.Circular(trailer_controller.model,np.array([0.2,0.2]),0.2)

    # construct right circle
    right_circle = obstacles.Circular(trailer_controller.model,np.array([0.7, 0.2]), 0.2)

    # add obstacles to controller
    trailer_controller.add_constraint(rectangular)
    trailer_controller.add_constraint(left_circle)
    trailer_controller.add_constraint(right_circle)

    # generate the dynamic code
    trailer_controller.generate_code()

    # simulate everything
    initial_state = np.array([0.45, 0.1,-math.pi/2])
    reference_state = np.array([0.8, -0.1, 0])
    reference_input = np.array([0, 0])

    obstacle_weights = [10000.,8000.,50.]

    state_history = simulate_demo(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights)

    plt.figure(0)
    example_models.trailer_print(state_history)
    rectangular.plot()
    left_circle.plot()
    right_circle.plot()
    plt.xlim([0, 1])
    plt.ylim([-0.3, 0.5])
    plt.xlabel('x')
    plt.xlabel('y')
    plt.title('Trailer')
    plt.savefig('demo1.png')
    plt.show()
    