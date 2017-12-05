import ctypes
from subprocess import call
import os
import platform
import subprocess
import numpy as np

class Simulator:
    """ simulator used to interact in python with an controller in c """
    def __init__(self,location):
        self._location=location
    def load_library(self):
        try:
            if (platform.system() == 'Linux'):
                print("Compiling python interface for Linux")
                extension_lib = '.so'
                lib_location = self._location + "libpython_interface" + extension_lib
                self.nmpc_python_interface = ctypes.CDLL(lib_location)
            elif (platform.system() == 'Windows'):
                extension_lib = '.dll'
                lib_location = self._location + "libpython_interface" + extension_lib
                print("Compiling python interface for Windows: " + lib_location)
                self.nmpc_python_interface = ctypes.windll.LoadLibrary(lib_location)
            else:
                print("ERROR platform can't be detected, using Linux")
                extension_lib = '.so'
        except:
            print("Failed to load the dll, are you sure python and the toolchain are compatible?")
            print("check if they both are either 32bit or both 64 bit")
    def simulate_nmpc(self,current_state,input_size):
        length_state = len(current_state)
        array_state = ctypes.c_double * length_state

        array_optimal_input = ctypes.c_double * input_size
        optimal_input = array_optimal_input()

        result = ctypes.c_double
        result = self.nmpc_python_interface.simulate_nmpc_panoc(\
            array_state(*current_state),\
            optimal_input\
            )
        # copy over the data in a numpy variable
        optimal_input_numpy = np.zeros((input_size,1))
        for i in range(0,input_size):
            optimal_input_numpy[i]=float(optimal_input[i])
        return (result, optimal_input_numpy)
    def simulator_init(self):
        self.compile_interface()
        self.load_library()
        self.nmpc_python_interface.simulation_init()
    def simulator_cleanup(self):
        self.nmpc_python_interface.simulation_cleanup()
    def compile_interface(self):
        cwd = os.getcwd()
        try:
            os.chdir(self._location)
            os.system("make clean python_interface")
        finally:
            os.chdir(cwd)
