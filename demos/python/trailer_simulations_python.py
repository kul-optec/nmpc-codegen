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
    Q = np.diag([1., 1., 1.])*0.2
    R = np.diag([1., 1.]) * 0.01

    Q_terminal = np.diag([1., 1., 1])*10
    R_terminal = np.diag([1., 1.]) * 0.01

    trailer_controller = prepare_demo_trailer(step_size,Q,R,Q_terminal,R_terminal)

    trailer_controller.horizon = 40 # NMPC parameter
    trailer_controller.integrator_casadi = True # optional  feature that can generate the integrating used  in the cost function
    trailer_controller.panoc_max_steps = 2000 # the maximum amount of iterations the PANOC algorithm is allowed to do.
    trailer_controller.min_residual=-3
    trailer_controller.lbgfs_buffer_size=50
    # trailer_controller.pure_prox_gradient=True

    # construct left circle
    circle1 = obstacles.Circular(trailer_controller.model,np.array([1.5,0.]),1.)
    circle2 = obstacles.Circular(trailer_controller.model,np.array([3.5, 2.]), 0.6)
    circle3 = obstacles.Circular(trailer_controller.model,np.array([2., 2.5]), 0.8)
    circle4 = obstacles.Circular(trailer_controller.model,np.array([5., 4.]), 1.05)

    # add obstacles to controller
    trailer_controller.add_constraint(circle1)
    trailer_controller.add_constraint(circle2)
    trailer_controller.add_constraint(circle3)
    trailer_controller.add_constraint(circle4)

    # generate the dynamic code
    trailer_controller.generate_code()

    # simulate everything
    initial_state = np.array([0., -0.5,math.pi/2])
    reference_state = np.array([7., 5., 0.8])
    reference_input = np.array([0, 0])

    obstacle_weights = [700.,700.,700.,700.]

    state_history = simulate_demo(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights)

    plt.figure(0)
    plt.clf()
    example_models.trailer_print(state_history)
    circle1.plot()
    circle2.plot()
    circle3.plot()
    circle4.plot()
    plt.xlim([-0.1, 7.1])
    plt.ylim([-0.1, 5.1])
    plt.xlabel('x')
    plt.xlabel('y')
    plt.title('Trailer')
    plt.savefig('trailer_simulations_python.png')
    plt.show()