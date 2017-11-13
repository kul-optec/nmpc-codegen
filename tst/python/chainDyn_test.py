# a simple test of the chain dynamics:
#  if the input is held at zero the chain should come to a resting position

from chainDyn import *
from integrators import *

# model parameters:
dimension=2
number_of_balls=5
ball_mass=1
spring_constant=1
rest_length_of_springs=2
gravity_acceleration=9.81

model_params = Chain_dyn_parameters(dimension,number_of_balls,ball_mass,
spring_constant,rest_length_of_springs,gravity_acceleration)

# initial state:
x0 = np.array([ 1.,0.,2.,0.,3.,0.,4.,0.,5.,0.,6.,0., 0.,0.,0.,0.,0. ])
x0 = x0.T

u0 = np.array([6,0])
function_system = lambda x: chain_dyn(x, u0, model_params)
# test = function_system(x0)
step_size=0.1
f_discreet = lambda x: integrator_explicit_euler(x,step_size,function_system)

current_state = f_discreet(x0)
print(current_state)
for i in range(1,10):
    current_state = f_discreet(current_state)
    print(current_state)