from Function import *

class ProximalFunction(Cfunction):
    def __init__(self,proxFunction):
        super.__init__(location_cfile)
        self._proxFunction=proxFunction
