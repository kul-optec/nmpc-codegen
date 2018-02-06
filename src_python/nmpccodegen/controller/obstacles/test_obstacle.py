import unittest
from .rectangular import Obstacle_rectangular
from .circle import Obstacle_circle
from .nonconvex_constraints import Obstacle_nonconvex_constraints
import numpy as np
import math

class TestObstaclesSquare(unittest.TestCase):
    def setUp(self):
        self.square_obstacle = Obstacle_rectangular(np.array([1.5,0]),1,2)
        self.circle_obstacle = Obstacle_circle(np.array([0, 0]), 1)

        # test on an costum obstacle
        self.costum_obstacle = Obstacle_nonconvex_constraints()
        h_0 = lambda x: x[1]-x[0]**2
        h_1 = lambda x: 1 + (x[0]**2)/2 - x[1]
        self.costum_obstacle.add_constraint(h_0)
        self.costum_obstacle.add_constraint(h_1)

        self.costum_obstacle2 = Obstacle_nonconvex_constraints()
        h_0 = lambda x: x[1] - 2. * math.sin(-x[0] / 2.)
        h_1 = lambda x: 3. * math.sin(x[0]/2. - 1.) - x[1]
        h_2 = lambda x: x[0] - 1.
        h_3 = lambda x: 8. - x[0]
        self.costum_obstacle2.add_constraint(h_0)
        self.costum_obstacle2.add_constraint(h_1)
        self.costum_obstacle2.add_constraint(h_2)
        self.costum_obstacle2.add_constraint(h_3)

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

    def test_zero_outside_costum(self):
        test_points = np.array([ \
            [0.,    0.,    1., -1.], \
            [-0.25, 1.25,  0.5, 0.5] \
            ])

        for i in range(0, 4):
            cost = np.asarray(self.costum_obstacle.evaluate_cost(test_points[:, i]))
            self.assertEqual(cost, 0., "error in testpoint " + str(i) + " --> " + str(test_points[:, i]))

    def test_zero_insideside_costum(self):
        test_points = np.array([ \
            [-0.5, 0.5, 0.], \
            [0.5, 0.5, 0.5] \
            ])

        for i in range(0, 3):
            cost = np.asarray(self.costum_obstacle.evaluate_cost(test_points[:, i]))
            self.assertGreater(cost, 0., "error in testpoint i=" + str(i) + " --> " + str(test_points[:, i]))

    def test_zero_outside_costum2(self):
        test_points = np.array([ \
            [2., 6., 7., 7.], \
            [2., -1., 3., -1.] \
            ])

        for i in range(0, 4):
            cost = np.asarray(self.costum_obstacle2.evaluate_cost(test_points[:, i]))
            self.assertEqual(cost, 0., "error in testpoint " + str(i) + " --> " + str(test_points[:, i]))

    def test_zero_insideside_costum2(self):
        test_points = np.array([ \
            [4., 5., 3.], \
            [1., 1., -1.] \
            ])

        for i in range(0, 3):
            cost = np.asarray(self.costum_obstacle2.evaluate_cost(test_points[:, i]))
            self.assertGreater(cost, 0., "error in testpoint i=" + str(i) + " --> " + str(test_points[:, i]))
# manual command = python3 -m unittest test_obstacle.py
if __name__== '__main__':
    unittest.main()