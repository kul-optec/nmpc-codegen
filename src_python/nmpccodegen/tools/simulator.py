import ctypes
from subprocess import call
import os
import platform
import subprocess
import numpy as np
import sys
class Simulation_data:
    def __init__(self,panoc_time,optimal_input):
        self._optimal_input=np.asarray(optimal_input)

        self._hours=panoc_time.hours
        self._minutes=panoc_time.minutes
        self._seconds=panoc_time.seconds

        self._milli_seconds=panoc_time.milli_seconds
        self._micro_seconds=panoc_time.micro_seconds
        self._nano_seconds=panoc_time.nano_seconds

        self._panoc_interations=panoc_time.panoc_interations

    @property
    def optimal_input(self):
        return self._optimal_input

    @property
    def time_string(self):
        return str(self._hours)+":"+str(self._minutes)+":"+str(self._seconds)+"  " \
               + str(self._milli_seconds)+":"+str(self._micro_seconds)+":"+str(self._nano_seconds)

    @property
    def hours(self):
        return self._hours
    @property
    def minutes(self):
        return self._minutes
    @property
    def seconds(self):
        return self._seconds
    @property
    def milli_seconds(self):
        return self._milli_seconds
    @property
    def micro_seconds(self):
        return self._micro_seconds
    @property
    def nano_seconds(self):
        return self._nano_seconds

    @property
    def panoc_interations(self):
        return self._panoc_interations



class Panoc_time(ctypes.Structure):
 _fields_ = [("hours", ctypes.c_int),("minutes", ctypes.c_int),("seconds", ctypes.c_int),\
             ("milli_seconds", ctypes.c_int),("micro_seconds", ctypes.c_int),("nano_seconds", ctypes.c_int),\
             ("panoc_interations", ctypes.c_int)
             ]


class Simulator:
    """ simulator used to interact in python with an controller in c """
    def __init__(self,nmpc_controller):
        self._nmpc_controller=nmpc_controller

    def _load_library(self):
        """ private function:load the compiled library into Python """
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

        # set return type: Panoc_time
        self.nmpc_python_interface.simulate_nmpc_panoc.restype = ctypes.POINTER(Panoc_time)

        convergence_time = self.nmpc_python_interface.simulate_nmpc_panoc(\
            array_state(*current_state),\
            optimal_input\
            )

        return Simulation_data(convergence_time[0],optimal_input)
    def simulator_init(self):
        self._compile_interface()
        self._load_library()
        self.nmpc_python_interface.simulation_init()
    def simulator_cleanup(self):
        self.nmpc_python_interface.simulation_cleanup()
    def _compile_interface(self):
        cwd = os.getcwd()
        try:
            os.chdir(self._nmpc_controller.location)
            os.system("make clean python_interface")
        finally:
            os.chdir(cwd)
