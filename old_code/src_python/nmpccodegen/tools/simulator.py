import ctypes
from subprocess import call
import os
import platform
import subprocess
import numpy as np
import sys
class Simulation_data:
    """
    Contains results of the simulator
    """
    def __init__(self,panoc_time,optimal_input):
        """
        crate simulation data

        Parameters
        ---------
        panoc_time : Time till convergence of PANOC
        optimal_input : The optimal input that should be applied to the system.
        """
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
    """
    Simulates the controller by compiling the C code into a
    dynamic library, and loading it into Matlab
       The simulator only works if the simulation tools were enabled when
       bootstrapping the environment.
    """
    def __init__(self,nmpc_controller_location,option=""):
        """
        Construct Simulator

        Parameters
        ---------
        nmpc_controller_location : 
        option : 3 different possibilities, leave empty/"using visual studio"/"not using visual studio"
        """
        self._nmpc_controller_location=nmpc_controller_location

        if (option == "visual studio"):
            self._visual_studio = True
            print("using visual studio")
        else:
            self._visual_studio = False
            print("not using visual studio")

        self._make_build_system()
        self._compile_interface()
        self._load_library()
        self.nmpc_python_interface.simulation_init()

    def __del__(self):
        self.nmpc_python_interface.simulation_cleanup()

    def simulate_nmpc(self,current_state,state_reference,input_reference):
        """
        Simulate the controller for 1 step

        Parameters
        ---------
        current_state : 
        state_reference : 
        input_reference : 

        Retuns
        -----
        Simulation_data object with simulation results in it
        """
        length_input_reference = len(input_reference)

        # construct an actual new array, and save a pointer to it
        array_optimal_input = ctypes.c_double * length_input_reference
        optimal_input = array_optimal_input()

        # set return type: Panoc_time
        self.nmpc_python_interface.simulate_nmpc_panoc.restype = ctypes.POINTER(Panoc_time)

        # get pointers to the numpy arrays
        c_double_p = ctypes.POINTER(ctypes.c_double)

        current_state = current_state.astype(np.float64)
        current_state_p = current_state.ctypes.data_as(c_double_p)

        state_reference = state_reference.astype(np.float64)
        state_reference_p = state_reference.ctypes.data_as(c_double_p)

        input_reference = input_reference.astype(np.float64)
        input_reference_p = input_reference.ctypes.data_as(c_double_p)

        convergence_time = self.nmpc_python_interface.simulate_nmpc_panoc(\
            current_state_p,\
            state_reference_p,\
            input_reference_p,\
            optimal_input\
            )

        return Simulation_data(convergence_time[0],optimal_input)
    def simulate_nmpc_multistep_solution(self,current_state,state_reference,input_reference,dimension_solution):
        """
        Simulate the controller for 1 step

        Parameters
        ---------
        current_state : 
        state_reference : 
        input_reference : 

        Retuns
        -----
        Simulation_data object with simulation results in it and the full horizon of optimal inputs
        --> return (sim_data,full_solution)
        """
        # simulate the controller
        sim_data = self.simulate_nmpc(current_state,state_reference,input_reference)
        input_size=len(input_reference)

        # get the full solution
        array_ctype_full_solution = ctypes.c_double * dimension_solution
        full_solution_ctype = array_ctype_full_solution()
        self.nmpc_python_interface.get_last_full_solution(full_solution_ctype)

        full_solution = np.zeros((dimension_solution,1))
        for i in range(0,dimension_solution):
            full_solution[i] = full_solution_ctype[i]

        return (sim_data,full_solution)

    def set_init_value_solver(self,value,index):
        """
        Set the initial horizon used 

        Parameters
        ---------
        value
        index
        """
        index_ctype = ctypes.c_int(index)
        value_ctype = ctypes.c_double(value)

        self.nmpc_python_interface.restype = ctypes.c_int

        self.nmpc_python_interface.simulation_set_buffer_solution(value_ctype,index_ctype)
    def set_weight_constraint(self,index_constraint,weight_constraint):
        """
        Set the weight of an constraint to an different weight than the
            default value.

        Parameters
        ---------
        index_constraint
        weight_constraint
        """
        index_constraint_ctype = ctypes.c_int(index_constraint)
        weight_constraint_ctype = ctypes.c_double(weight_constraint)

        self.nmpc_python_interface.simulation_set_weight_constraints(index_constraint_ctype,weight_constraint_ctype)

    def get_last_buffered_cost(self):
        """
        Returns the most recent cost of the full horizon

        """
        self.nmpc_python_interface.get_last_buffered_cost.restype = ctypes.c_double
        return self.nmpc_python_interface.get_last_buffered_cost()

    def _make_build_system(self):
        """
        Construct the build system (make files or visual studio solution)
        """
        cwd = os.getcwd()
        try:
            os.chdir(self._nmpc_controller_location)
            if (platform.system() == 'Linux'):
                os.system(" cmake -H. -Bbuild")
            elif (platform.system() == 'Windows'):
                if(self._visual_studio):
                    os.system("cmake -H. -Bbuild -DCMAKE_GENERATOR_PLATFORM=x64")
                else:
                    os.system("cmake -H. -Bbuild -G \"MinGW Makefiles\"")
            elif (platform.system() == 'Darwin'):
                os.system(" cmake -H. -Bbuild ")
            else:
                print("ERROR Platform not supported use either Linux,Mac or Windows")
        finally:
            os.chdir(cwd)
    def _compile_interface(self):
        """
        Compile the Python/Matlab
        """
        cwd = os.getcwd()
        try:
            os.chdir(self._nmpc_controller_location)
            os.system("cmake --build ./build --config Release --target python_interface")
        finally:
            os.chdir(cwd)
    def _load_library(self):
        """ 
        Load the compiled library into Python 
        """
        self._make_build_system()
        try:
            if (platform.system() == 'Linux'):
                print("Compiling python interface for Linux")
                extension_lib = '.so'
                lib_location = self._nmpc_controller_location + "/build/libpython_interface" + extension_lib
                self.nmpc_python_interface = ctypes.CDLL(lib_location)
            elif (platform.system() == 'Windows'):
                if(self._visual_studio):
                    extension_lib = '.dll'
                    lib_location = self._nmpc_controller_location + "/build/Release/libpython_interface" + extension_lib
                    print("Compiling python interface for Windows using Visual Studio toolset: " + lib_location)
                else:
                    extension_lib = '.dll'
                    lib_location = self._nmpc_controller_location + "/build/libpython_interface" + extension_lib
                    print("Compiling python interface for Windows using MINGW: " + lib_location)
                self.nmpc_python_interface = ctypes.windll.LoadLibrary(lib_location)
            elif(platform.system() == 'Darwin'):
                print("Compiling python interface for Mac")
                extension_lib = '.dylib'
                lib_location = self._nmpc_controller_location + "/build/libpython_interface" + extension_lib
                self.nmpc_python_interface = ctypes.CDLL(lib_location)
            else:
                print("ERROR platform can't be detected, using Linux")
                extension_lib = '.so'
                lib_location = self._nmpc_controller_location + "/build/libpython_interface" + extension_lib
                self.nmpc_python_interface = ctypes.CDLL(lib_location)
        except:
            print("Failed to load the dll, are you sure python and the toolchain are compatible?")
            print("check if they both are either 32bit or both 64 bit")
