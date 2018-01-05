import unittest
import obstacle as obs
import numpy as np

class TestObstaclesSquare(unittest.TestCase):
    def setUp(self):
        x_up = 2.
        x_down = 1.
        y_up = 1.
        y_down = -1.
        self.square_obstacle = obs.Basic_obstacles.generate_rec_object(x_up, x_down, y_up, y_down)

    def test_zero_outside_square(self):
        test_points=np.array([[0.9, 1.5,2.5,-1.5],[0,1.5,0,-1.5]])

        for i in range(0,4):
            cost = np.asarray(self.square_obstacle.evaluate_cost(test_points[:,i]))
            self.assertEqual(cost[0,0],0.,"error in testpoint "+str(i)+" --> "+str(test_points[:,i]))

    def test_zero_insideside_square(self):
        test_points=np.array([\
                                [1.1, 1.5 ,1.9, 1.5 ],\
                                [0  , 0.9 ,0  , -0.9 ]\
                              ])

        for i in range(0,4):
            cost = np.asarray(self.square_obstacle.evaluate_cost(test_points[:,i]))
            self.assertGreater(cost[0,0],0.,"error in testpoint i="+str(i)+" --> "+str(test_points[:,i]))


# manual command = python3 -m unittest test_obstacle.py
if __name__== '__main__':
    unittest.main()