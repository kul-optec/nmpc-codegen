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
    step_size=0.03

    # Q and R matrixes determined by the control engineer.
    Q = np.diag([1., 1., 0.0])*0.2
    R = np.diag([1., 1.]) * 0.01

    Q_terminal = np.diag([1., 1., 0.0])*2
    R_terminal = np.diag([1., 1.]) * 0.01

    trailer_controller = prepare_demo_trailer(step_size,Q,R,Q_terminal,R_terminal)

    trailer_controller.horizon = 50 # NMPC parameter
    trailer_controller.integrator_casadi = True # optional  feature that can generate the integrating used  in the cost function
    trailer_controller.panoc_max_steps = 500 # the maximum amount of iterations the PANOC algorithm is allowed to do.
    trailer_controller.min_residual=-3

    # construct left circle
    left_circle = obstacles.Circular(trailer_controller.model,np.array([0.2,0.2]),0.2)

    # construct right circle
    right_circle = obstacles.Circular(trailer_controller.model,np.array([0.7, 0.2]), 0.2)

    # add obstacles to controller
    trailer_controller.add_constraint(left_circle)
    trailer_controller.add_constraint(right_circle)

    # generate the dynamic code
    trailer_controller.generate_code()

    # simulate everything
    initial_state = np.array([0.2, 0.6, 0])
    reference_state = np.array([0.7, -0.02, math.pi/2])
    reference_input = np.array([0, 0])

    obstacle_weights = [1000.,1000.]

    state_history = simulate_demo(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights)

    plt.figure(0)
    example_models.trailer_print(state_history)
    left_circle.plot()
    right_circle.plot()
    plt.xlim([0, 1])
    plt.ylim([-0.3, 1])
    plt.xlabel('x')
    plt.xlabel('y')
    plt.title('Trailer')
    plt.show()