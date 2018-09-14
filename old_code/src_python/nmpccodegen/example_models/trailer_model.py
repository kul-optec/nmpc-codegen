# import math
import casadi as cd
import numpy as np

class Trailer_model:
    def __init__(self,L):
        self._L=L
    def system_equation(self,x,u):
        theta_dot = (-u[0] * cd.sin(x[2]) + u[1] * cd.cos(x[2])) / self._L
        px_dot = ( u[0] + self._L * cd.sin(x[2] ) * theta_dot)
        py_dot = ( u[1] - self._L * cd.cos(x[2] ) * theta_dot)

        x_dot = cd.vertcat(px_dot, py_dot, theta_dot)

        return x_dot

def main():
    initial_state = np.array([0., 0., 0.])
    input = np.array([1., 1.])

    tm = Trailer_model(L=0.5)
    test = tm.system_equation(initial_state, input)

    print(test)

if __name__ == "__main__":
    main()