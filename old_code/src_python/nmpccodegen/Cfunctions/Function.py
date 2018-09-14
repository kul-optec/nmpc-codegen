class Cfunction:
    """
    Abstact class representing any function that has a implementation in c89
    """
    def __init__(self):
        raise NotImplementedError

    # save the implementation in c to "location"
    def generate_c_code(self,location):
        raise NotImplementedError
