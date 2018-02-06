import unittest
from .basic_2D_obstacles import Basic_2D_obstacles
from .rectangular import Obstacle_rectangular
from .circle import Obstacle_circle
import numpy as np

class TestObstaclesSquare(unittest.TestCase):
    def setUp(self):
        self.square_obstacle = Obstacle_rectangular(np.array([1.5,0]),1,2)
        self.circle_obstacle = Obstacle_circle(np.array([0, 0]), 1)

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

    def test_zero_outside_circle(self):
        test_points = np.array([\
                [1., -1., 1., -1.],\
                [1., -1., -1., 1.]\
            ])

        for i in range(0, 4):
            cost = np.asarray(self.circle_obstacle.evaluate_cost(test_points[:, i]))
            self.assertEqual(cost[0, 0], 0., "error in testpoint " + str(i) + " --> " + str(test_points[:, i]))

    def test_zero_insideside_circle(self):
        test_points = np.array([ \
            [0, 0.5, -0.5, -.05, 0.5], \
            [0, 0.5, -0.5, 0.5, -0.5] \
            ])

        for i in range(0, 5):
            cost = np.asarray(self.circle_obstacle.evaluate_cost(test_points[:, i]))
            self.assertGreater(cost[0, 0], 0., "error in testpoint i=" + str(i) + " --> " + str(test_points[:, i]))


# manual command = python3 -m unittest test_obstacle.py
if __name__== '__main__':
    unittest.main()