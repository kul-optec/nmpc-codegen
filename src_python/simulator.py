import ctypes

class Simulator:
    """ simulator used to interact in python with an controller in c """
    def __init__(self,location):
        self.nmpc_python_interface = ctypes.CDLL(location+"libpython_interface.so")
        self._location=location

        # self.nmpc_python_interface.simulation_init.argtypes = ()
        # self.nmpc_python_interface.simulate_nmpc_panoc.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
        # self.nmpc_python_interface.simulation_cleanup.argtypes = ()

        self.simulator_init()
    def simulate_nmpc(self,current_state,input_size):
        # global nmpc_python_interface       
        length_state = len(current_state)
        array_state = ctypes.c_double * length_state

        array_optimal_input = ctypes.c_double * input_size
        optimal_input = array_optimal_input()

        # result = self.nmpc_python_interface.simulate_nmpc_panoc(array_state(*current_state), array_optimal_input(*optimal_input))

        result = ctypes.c_double
        result = self.nmpc_python_interface.simulate_nmpc_panoc(\
            array_state(*current_state),\
            optimal_input\
            )
        print(type(result))
        return (result, optimal_input)
    def simulator_init(self):
        self.nmpc_python_interface.simulation_init()
    def simulator_cleanup(self):
        self.nmpc_python_interface.simulation_cleanup()