from .Function import Cfunction

class ProximalFunction(Cfunction):
    """
    Class that represents a function with its proximal mapping
    """
    def __init__(self,prox):
        self._prox=prox

    @property
    def prox(self):
        return self._prox
