import math
import numpy as np
import matplotlib.pyplot as plt

# little hack to import the local lib and not work with the one in the path
import sys
sys.path.insert(0, '../../src_python')
import nmpc_panoc as npc
import model_continious as modelc
import example_models # this contains the chain example

model = example_models.get_chain_model()
horizon=10
dimension=2

Q = np.diag([0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])*10
R = np.eye(model.number_of_inputs, model.number_of_inputs)

rest_state = np.array([0.1932, -5.9190 , 0.3874,-8.8949,0.6126,-8.8949,0.8068,-5.9190 \
                        ,1. , 0., \
                        0.,0., 0.,0.,0.,0.,0.,0.])
input=np.zeros((horizon*dimension,1))

nmpc_controller = npc.Nmpc_panoc("../../",model,Q,R)
nmpc_controller.horizon=10

nmpc_controller.generate_code()

cost_function = nmpc_controller.cost_function
print(cost_function(rest_state,input))
print(cost_function(rest_state*0.8,input))
print(cost_function(rest_state*1.5,input))