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
    Q = np.diag([1., 1., 0.0])*0.2
    R = np.diag([1., 1.]) * 0.01

    trailer_controller = prepare_demo_trailer(step_size,Q,R)

    trailer_controller.horizon = 50 # NMPC parameter
    trailer_controller.integrator_casadi = True # optional  feature that can generate the integrating used  in the cost function
    trailer_controller.panoc_max_steps = 2000 # the maximum amount of iterations the PANOC algorithm is allowed to do.
    trailer_controller.min_residual=-3
    trailer_controller.lbgfs_buffer_size = 50
    # trailer_controller.pure_prox_gradient=True

    # construct upper rectangular
    rectangular_up = obstacles.Rectangular(trailer_controller.model,np.array([1,0.5]),0.4,0.5)

    # construct lower rectangular
    rectangular_down = obstacles.Rectangular(trailer_controller.model,np.array([1, -0.2]), 0.4, 0.5)

    # construct circle
    circle = obstacles.Circular(trailer_controller.model,np.array([0.2,0.2]),0.2)

    # add obstacles to controller
    trailer_controller.add_constraint(rectangular_up)
    trailer_controller.add_constraint(rectangular_down)
    trailer_controller.add_constraint(circle)

    # generate the dynamic code
    trailer_controller.generate_code()

    # simulate everything
    initial_state = np.array([-0.1, -0.1,math.pi/4])
    reference_state = np.array([1.5, 0.4, 0])
    reference_input = np.array([0, 0])

    obstacle_weights = [1e3,1e3,1e3]

    state_history = simulate_demo(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights)

    plt.figure(0)
    example_models.trailer_print(state_history)
    circle.plot()
    rectangular_up.plot()
    rectangular_down.plot()
    plt.xlim([-0.2, 1.6])
    plt.ylim([-0.5, 1.])
    plt.xlabel('x')
    plt.xlabel('y')
    plt.title('Trailer')
    plt.savefig('OneCricleTwoRectTrailer.png')
    plt.show()