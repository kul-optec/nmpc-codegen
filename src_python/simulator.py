import ctypes
from subprocess import call
import os
import platform
import subprocess
import numpy as np
import sys

class Simulator:
    """ simulator used to interact in python with an controller in c """
    def __init__(self,nmpc_controller):
        self._nmpc_controller=nmpc_controller

    def load_library(self):
        try:
            if (platform.system() == 'Linux'):
                print("Compiling python interface for Linux")
                extension_lib = '.so'
                lib_location = self._nmpc_controller.location + "libpython_interface" + extension_lib
                self.nmpc_python_interface = ctypes.CDLL(lib_location)
            elif (platform.system() == 'Windows'):
                extension_lib = '.dll'
                lib_location = self._nmpc_controller.location + "libpython_interface" + extension_lib
                print("Compiling python interface for Windows: " + lib_location)
                self.nmpc_python_interface = ctypes.windll.LoadLibrary(lib_location)
            else:
                print("ERROR platform can't be detected, using Linux")
                extension_lib = '.so'
        except:
            print("Failed to load the dll, are you sure python and the toolchain are compatible?")
            print("check if they both are either 32bit or both 64 bit")
        sys.stdout.flush()
    def simulate_nmpc(self,current_state):
        length_state = len(current_state)
        array_state = ctypes.c_double * length_state

        array_optimal_input = ctypes.c_double * self._nmpc_controller.model.number_of_inputs
        optimal_input = array_optimal_input()

        result = ctypes.c_double
        result = self.nmpc_python_interface.simulate_nmpc_panoc(\
            array_state(*current_state),\
            optimal_input\
            )

        return (result, np.asarray(optimal_input))
    def simulator_init(self):
        self.compile_interface()
        self.load_library()
        self.nmpc_python_interface.simulation_init()
    def simulator_cleanup(self):
        self.nmpc_python_interface.simulation_cleanup()
    def compile_interface(self):
        cwd = os.getcwd()
        try:
            os.chdir(self._nmpc_controller.location)
            os.system("make clean python_interface")
        finally:
            os.chdir(cwd)
