import sys
sys.path.insert(0, '../../../src_python')
import nmpccodegen.controller as controller

from trailer_generate_controller import generate_controller
from trailer_generate_controller_with_obs import generate_controller_with_obs

import unittest
import numpy as np

class TestTrailerController(unittest.TestCase):
    def test_move_up(self):
        reference_state=np.array([0,2,0])
        current_state = generate_controller("trailer_move_up",reference_state,display_figure=False)
        self.check_with_reference(reference_state,current_state,accuracy=0.01)

    def test_move_right(self):
        reference_state=np.array([2,0,0])
        current_state = generate_controller("trailer_move_right",reference_state,display_figure=False)
        self.check_with_reference(reference_state,current_state,accuracy=0.01)

    def test_move_diag(self):
        reference_state=np.array([2,0,0])
        current_state = generate_controller("trailer_move_diag",reference_state,display_figure=False)
        self.check_with_reference(reference_state,current_state,accuracy=0.01)

    def test_move_diag_obs(self):
        # TEST 1
        x_up = 1.
        x_down = 0.5
        y_up = 0.6
        y_down = 0.3
        obstacle = controller.Basic_obstacles.generate_rec_object(x_up, x_down, y_up, y_down)

        Q = np.diag([1., 100., 1.])
        obstacle_weight = 10000000000000.
        # obstacle_weight=0
        horizon = 300

        reference_state = np.array([2, 0.5, 0])
        current_state = generate_controller_with_obs("trailer_move_diag_obs", reference_state, Q, obstacle,
                                                     obstacle_weight,
                                                     horizon,display_figure=False)
        self.check_with_reference(reference_state, current_state,accuracy=0.1)
    def test_move_right_obs(self):
        # TEST 2
        x_up = 1.
        x_down = 0.5
        y_up = 0.2
        y_down = -0.2
        obstacle = controller.Basic_obstacles.generate_rec_object(x_up, x_down, y_up, y_down)

        Q = np.diag([10., 1., 1.])
        obstacle_weight = 10000000000000.
        horizon = 100

        reference_state = np.array([2, 0, 0])
        current_state = generate_controller_with_obs("trailer_move_right_obs", reference_state, Q, obstacle,
                                                     obstacle_weight, horizon,display_figure=False)
        self.check_with_reference(reference_state, current_state, accuracy=0.1)
    def test_move_up_obs(self):
        # TEST 3
        x_up = 1
        x_down = -1
        y_up = 0.6
        y_down = 0.4
        obstacle = controller.Basic_obstacles.generate_rec_object(x_up, x_down, y_up, y_down)

        Q = np.diag([1., 1000., 1.])
        obstacle_weight = 10000000.
        horizon = 100

        reference_state = np.array([0, 2, 0])
        current_state = generate_controller_with_obs("trailer_move_up_obs", reference_state, Q, obstacle,
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