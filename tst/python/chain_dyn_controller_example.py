from chainDynCasadi import *
from integrators import *
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

Q = np.eye(model.number_of_states, model.number_of_states)
R = np.eye(model.number_of_inputs, model.number_of_inputs)

nmpc_controller = npc.Nmpc_panoc("../../",model,Q,R)
nmpc_controller.generate_code()