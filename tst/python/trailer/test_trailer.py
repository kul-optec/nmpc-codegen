import unittest
import trailer_generate_controller as tgc
import numpy as np

class TestTrailerController(unittest.TestCase):
    def test_move_up(self):
        reference_state=np.array([0,2,0])
        current_state = tgc.generate_controller("trailer_move_up",reference_state,display_figure=False)
        self.check_with_reference(reference_state,current_state)

    def test_move_right(self):
        reference_state=np.array([2,0,0])
        current_state = tgc.generate_controller("trailer_move_right",reference_state,display_figure=False)
        self.check_with_reference(reference_state,current_state)    

    def test_move_diag(self):
        reference_state=np.array([2,0,0])
        current_state = tgc.generate_controller("trailer_move_diag",reference_state,display_figure=False)
        self.check_with_reference(reference_state,current_state)   

    def check_with_reference(self,reference_state,current_state):
        difference=abs(reference_state[0]-current_state[0][0])
        error_message = "x position is not equal to reference, the difference is:" + str(difference)
        self.assertTrue(difference<0.001,error_message)

        difference=abs(reference_state[1]-current_state[1][0])
        error_message = "y position is not equal to reference, the difference is:" + str(difference)
        self.assertTrue(difference<0.001,error_message)

        difference=abs(reference_state[2]-current_state[2][0])
        error_message = "angle(theta) is not equal to reference, the difference is:" + str(difference)
        self.assertTrue(difference<0.001,error_message)

# manual command = python3 -m unittest test_trailer.py
if __name__== '__main__':
    unittest.main()