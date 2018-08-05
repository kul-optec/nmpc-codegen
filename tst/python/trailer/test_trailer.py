import sys
sys.path.insert(0, '../../../src_python')
import nmpccodegen.controller as controller

from trailer_generate_controller import generate_controller
from trailer_generate_controller_with_obs import generate_controller_with_obs
import nmpccodegen.controller.obstacles as obstacles

import unittest
import numpy as np

class TestTrailerController(unittest.TestCase):
    def test_move_up(self):
        reference_state=np.array([0,2,0])
        horizon = 50
        panoc_max_steps = 3000
        current_state = generate_controller("trailer_move_up",reference_state,horizon,panoc_max_steps,display_figure=False)
        self.check_with_reference(reference_state,current_state,accuracy=0.01)

    def test_move_right(self):
        reference_state=np.array([2,0,0])
        horizon = 50
        panoc_max_steps = 1000
        current_state = generate_controller("trailer_move_right",reference_state,horizon,panoc_max_steps,display_figure=False)
        self.check_with_reference(reference_state,current_state,accuracy=0.01)

    def test_move_diag(self):
        reference_state=np.array([2,0,0])
        horizon = 50
        panoc_max_steps = 1000
        current_state = generate_controller("trailer_move_diag",reference_state,horizon,panoc_max_steps,display_figure=False)
        self.check_with_reference(reference_state,current_state,accuracy=0.01)

    def test_move_diag_obs(self):
        # TEST 1
        rectangular_center_coordinates = np.array([0.75, 0.45])
        rectangular_width = 0.5
        rectangular_height = 0.3
        rectangular_obstacle_1 = obstacles.Obstacle_rectangular(rectangular_center_coordinates, \
                                                                rectangular_width, rectangular_height)

        Q = np.diag([10., 10., 1.])
        R = np.diag([1., 1.]) * 0.01
        obstacle_weight = 10000.
        horizon = 50

        reference_state = np.array([2, 0.5, 0])

        reference_state = np.array([2, 0.5, 0])
        current_state = generate_controller_with_obs("trailer_move_diag_obs", reference_state, Q, R, rectangular_obstacle_1,
                                                     obstacle_weight,
                                                     horizon,display_figure=False)
        self.check_with_reference(reference_state, current_state,accuracy=0.1)
    def test_move_right_obs(self):
        # TEST 2
        rectangular_center_coordinates_2 = np.array([1, 0.])
        rectangular_width_2 = 0.5
        rectangular_height_2 = 0.2
        rectangular_obstacle_2 = obstacles.Obstacle_rectangular(rectangular_center_coordinates_2, \
                                                                rectangular_width_2, rectangular_height_2)

        Q = np.diag([10., 10., 1.]) * 1.
        R = np.diag([1., 1.]) * 0.01
        obstacle_weight = 1000.
        horizon = 50

        reference_state = np.array([2, 0, 0])
        current_state = generate_controller_with_obs("trailer_move_right_obs", reference_state, Q, R, rectangular_obstacle_2,
                                                     obstacle_weight, horizon,display_figure=False)
        self.check_with_reference(reference_state, current_state, accuracy=0.1)
    def test_move_up_obs(self):
        # TEST 3
        rectangular_center_coordinates = np.array([0.6, 0.5])
        rectangular_width = 1.2
        rectangular_height = 0.2
        rectangular_obstacle_3 = obstacles.Obstacle_rectangular(rectangular_center_coordinates, \
                                                                rectangular_width, rectangular_height)

        Q = np.diag([10., 10., 0.1])
        R = np.diag([1., 1.]) * 0.01
        obstacle_weight = 10000.
        horizon = 50

        reference_state = np.array([0, 2, 0])
        current_state = generate_controller_with_obs("trailer_move_up_obs", reference_state, Q,R, rectangular_obstacle_3,
                                                     obstacle_weight, horizon,display_figure=False)

        self.check_with_reference(reference_state, current_state, accuracy=0.1)
    def check_with_reference(self,reference_state,current_state,accuracy):
        difference=abs(reference_state[0]-current_state[0][0])
        error_message = "x position is not equal to reference, the difference is:" + str(difference)
        self.assertTrue(difference<accuracy,error_message)

        difference=abs(reference_state[1]-current_state[1][0])
        error_message = "y position is not equal to reference, the difference is:" + str(difference)
        self.assertTrue(difference<accuracy,error_message)

        difference=abs(reference_state[2]-current_state[2][0])
        error_message = "angle(theta) is not equal to reference, the difference is:" + str(difference)
        self.assertTrue(difference<accuracy,error_message)

# manual command = python3 -m unittest test_trailer.py
if __name__== '__main__':
    unittest.main()