from Cfunctions.Function import *

class ProximalFunction(Cfunction):
    def __init__(self,prox):
        self._prox=prox

    @property
    def prox(self):
        return self._prox
