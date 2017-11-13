import numpy as np

class Chain_dyn_parameters:
    """ chain dynamic model parameters """
    def __init__(self,dimension,number_of_balls,ball_mass,spring_constant,
    rest_length_of_springs,gravity_acceleration):
        self._dimension=dimension # dim
        self._number_of_balls=number_of_balls # M
        self._ball_mass=ball_mass # m
        self._spring_constant=spring_constant # D
        self._rest_length_of_springs=rest_length_of_springs # L
        self._gravity_acceleration=gravity_acceleration # g
    @property
    def dimension(self):
        return self._dimension
    @property
    def number_of_balls(self):
        return self._number_of_balls
    @property
    def ball_mass(self):
        return self._ball_mass
    @property
    def spring_constant(self):
        return self._spring_constant
    @property
    def rest_length_of_springs(self):
        return self._rest_length_of_springs
    @property
    def gravity_acceleration(self):
        return self._gravity_acceleration
    # properties calculated based on model parameters
    @property
    def number_of_states(self):
        return self._dimension*(2*self._number_of_balls+1)
    @property
    def number_of_inputs(self):
        return self._dimension*(2*self._number_of_balls+1)
    @property
    def number_of_outputs(self):
        return self._dimension*(self._number_of_balls+1)

# x: state vector [pos_1, ..., pos_M, pos_{M+1}, vel_1, ..., vel_M]
# u: input vector
def chain_dyn(x, u, model_parameters):   
    """ returns the derivative of the state dx=f(x) """
    
    positions = np.transpose(np.reshape( x[0:model_parameters.dimension*(model_parameters.number_of_balls+1)] , 
                [ model_parameters.number_of_balls+1 , model_parameters.dimension]))

    # compute distance between masses
    distance_between_balls =  np.subtract(positions[0:model_parameters.dimension,1:model_parameters.number_of_balls+1] , positions[0:model_parameters.dimension,0:model_parameters.number_of_balls])

    # add the distance(and its norm) between the first ball and the fixed wall
    distance_between_balls = np.concatenate( (positions[0:model_parameters.dimension,0].reshape(model_parameters.dimension,1) , distance_between_balls), axis=1)
    distance_between_balls_norm = np.sqrt(np.sum(distance_between_balls**2,axis=0))

    # calculate force between balls on springs
    F=model_parameters.spring_constant*(1-model_parameters.rest_length_of_springs/distance_between_balls_norm)*(distance_between_balls)


    # find acceleration
    acceleration=(1/model_parameters.ball_mass)*\
        	(F[:,1:]-F[:,0:model_parameters.number_of_balls])\
              + model_parameters.gravity_acceleration

    x_dot = np.concatenate((positions,np.reshape(u,[2,1]),acceleration),axis=1)
    x_dot = np.reshape(np.dstack((x_dot)),[1,model_parameters.dimension*model_parameters.number_of_outputs])

    return x_dot

def main():
    print("Simple demo chain dynamics with 5 masses:")
    # model parameters:
    dimension=2
    number_of_balls=5
    ball_mass=1
    spring_constant=1
    rest_length_of_springs=2
    gravity_acceleration=9.81

    model_params = Chain_dyn_parameters(dimension,number_of_balls,ball_mass,
    spring_constant,rest_length_of_springs,gravity_acceleration)

    # initial state:
    x0 = np.array([ 1.,0.,2.,0.,3.,0.,4.,0.,5.,0.,6.,0., 0.,0.,0.,0.,0. ])
    x0 = x0.T
    u0 = np.array([6,0])

    # call the chain dyn function with intial state
    x0_dot = chain_dyn(x0, u0, model_params)
  
if __name__== "__main__":
  main()
