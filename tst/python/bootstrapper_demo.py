# little hack to import the local lib and not work with the one in the path
import sys
sys.path.insert(0, '../../src_python')
import nmpc_panoc as npc
import model_continious as modelc
import example_models # this contains the chain example

import ctypes
import simulator
import numpy as np
import matplotlib.pyplot as plt
import math
import Cfunctions.IndicatorBoxFunction as indbox
import bootstrapper as bs

location_nmpc_repo = "../.."
location = location_nmpc_repo+"/test_controller_builds"
controller_name = "_test_controller"

bs.Bootstrapper_panoc_nmpc.bootstrap(location_nmpc_repo,location,controller_name,python_interface_enabled=True)