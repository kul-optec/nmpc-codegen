class Nmpc_panoc:
    """ Defines a nmpc problem of the shape min f(x)+ g(x) """
    def __init__(self, location_lib,f,(g,proxg)):
        self._location_lib=location_lib # location of the library
        raise NotImplementedError # class needs further implementation
    def generate_code():
        """ Generate code controller """
        raise NotImplementedError
    def simulation():
        """ Simulate the controller """
        self.generate_code()
        # TODO call the make file
        raise NotImplementedError
    def generate_minimum_lib(location):
        """ Generate a lib with minimum amount of files  """
        raise NotImplementedError
