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

from demo import prepare_demo_trailer,simulate_demo,draw_obstacle_border

if __name__ == '__main__':
    step_size=0.025

    # Q and R matrixes determined by the control engineer.
    Q = np.diag([1., 1., 0.1])*2
    R = np.diag([1., 1.]) * 0.01

    Q_terminal = np.diag([1., 1., 0.1])*10
    R_terminal = np.diag([1., 1.]) * 0.01

    trailer_controller = prepare_demo_trailer(step_size,Q,R,Q_terminal,R_terminal)

    trailer_controller.horizon = 50 # NMPC parameter
    trailer_controller.integrator_casadi = True # optional  feature that can generate the integrating used  in the cost function
    trailer_controller.panoc_max_steps = 2000 # the maximum amount of iterations the PANOC algorithm is allowed to do.
    trailer_controller.min_residual=-3
    trailer_controller.lbgfs_buffer_size = 10
    # trailer_controller.pure_prox_gradient = True  # this will ignore the lbgfs, only usefull when testing !!!

    # construct upper rectangular
    costum_obstacle = obstacles.Nonconvex_constraints(trailer_controller.model)
    h_0 = lambda x: x[1] - 2.*math.sin(-x[0]/2.)
    h_1 = lambda x: 3.*math.sin(x[0]/2 -1) - x[1]
    h_2 = lambda x: x[0] - 1
    h_3 = lambda x: 8 - x[0]
    costum_obstacle.add_constraint(h_0)
    costum_obstacle.add_constraint(h_1)
    costum_obstacle.add_constraint(h_2)
    costum_obstacle.add_constraint(h_3)

    # add obstacles to controller
    trailer_controller.add_constraint(costum_obstacle)

    # generate the dynamic code
    trailer_controller.generate_code()

    # simulate everything
    initial_state = np.array([7, -1,0])
    reference_state = np.array([1.5, -2., 0])
    reference_input = np.array([0, 0])

    obstacle_weights = [1e1]

    state_history = simulate_demo(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights)

    plt.figure(0)
    example_models.trailer_print(state_history)
    h_0_border = lambda x: 2.*math.sin(-x/2.)
    h_1_border = lambda x: 3.*math.sin(x/2. -1.)
    draw_obstacle_border(h_0_border,[1,8],100)
    draw_obstacle_border(h_1_border, [1, 8], 100)
    plt.xlim([0, 9])
    plt.ylim([-3, 4])
    plt.xlabel('x')
    plt.xlabel('y')
    plt.title('Trailer')
    plt.savefig('demo4.png')
    plt.show()