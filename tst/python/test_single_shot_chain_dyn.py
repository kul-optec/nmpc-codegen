import math
import numpy as np
import matplotlib.pyplot as plt

# little hack to import the local lib and not work with the one in the path
import sys
sys.path.insert(0, '../../src_python')
import nmpc_panoc as npc
import model_continious as modelc
import example_models # this contains the chain example
import stage_costs
import Cfunctions.IndicatorBoxFunction as indbox

(system_equations, number_of_states, number_of_inputs) = example_models.get_chain_model()
dimension = 2
number_of_balls = 4

step_size = 0.01
simulation_time = 5
number_of_steps = math.ceil(simulation_time / step_size)
horizon = number_of_steps

integrator = "RK"
constraint_input = indbox.IndicatorBoxFunction([-2,-2],[2,2]) # input needs stay within these borders
model = modelc.Model_continious(system_equations, constraint_input, step_size, number_of_states,\
                                number_of_inputs, integrator)

Q = np.diag([0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])*10
R = np.eye(model.number_of_inputs, model.number_of_inputs)

rest_state = np.array([0.1932, -5.9190 , 0.3874,-8.8949,0.6126,-8.8949,0.8068,-5.9190 \
                        ,1. , 0., \
                        0.,0., 0.,0.,0.,0.,0.,0.])
input=np.zeros((horizon*dimension,1))

stage_cost = stage_costs.Stage_cost_QR(model,Q,R)
# define the controller
nmpc_controller_location = "../../"
nmpc_controller = npc.Nmpc_panoc(nmpc_controller_location,model,stage_cost )
nmpc_controller.horizon=10

nmpc_controller.generate_code()

cost_function = nmpc_controller.cost_function
print(cost_function(rest_state*0.8,input))
print(cost_function(rest_state,input))
print(cost_function(rest_state*1.5,input))

print("---")

cost_function = nmpc_controller.cost_function_derivative

derivative_cost_low=cost_function(rest_state*0.8,input)
derivative_cost_optimal=cost_function(rest_state,input)
derivative_cost_high=cost_function(rest_state*1.5,input)

print_size=2
print(derivative_cost_low[0:print_size])
print(derivative_cost_optimal[0:print_size])
print(derivative_cost_high[0:print_size])