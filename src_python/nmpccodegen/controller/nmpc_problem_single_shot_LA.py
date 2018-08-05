import casadi as cd
from .casadi_code_generator import Casadi_code_generator as ccg

class Single_shot_LA_definition:
    """ 
    single shot nmpc defintion 
    """
    def __init__(self,controller):
        self._controller=controller
        self._dimension=controller.model.number_of_inputs*controller.horizon

    def generate_cost_general_constraints(self, current_state, input, lambdas, general_constraint_weights,
                                          step_horizon):
        """ 
        Evaluate function cost of all general constraints for 1 step in the horizon
            L = lambda ci(x) + mu ci(x)^2

        Parameters
        ---------
        current_state: state of this step in the horizon
        input: current input applied to the system
        lambdas: lambda's for this step of the horizon
        general_constraint_weights: mu's for this step of the horizon
        step_horizon: the index of the step in the horizon (the first step is index 0)
        number_of_general_constraints = length(obj.controller.general_constraints);
        """
        offset_constraints = step_horizon * self._controller.number_of_general_constraints
        cost = cd.SX(1, 1)
        for i in range(0, self._controller.number_of_general_constraints):
            constraint_cost = self._controller.general_constraints[i].evaluate_cost(current_state, input)
            cost = cost - constraint_cost * lambdas[offset_constraints + i]
            cost = cost + (constraint_cost ** 2) * general_constraint_weights[offset_constraints + i]

        return cost

    def evaluate_constraints(self, state, input, constraint_values, step_horizon):
        """ 
        Evaluate cost of general constraints for 1 step in the horizon

        Parameters
        ---------
        state: state of this step in the horizon
        input: current input applied to the system
        constraint_values: contains the costs of the constraints
        step_horizon: the index of the step in the horizon (the first step is index 0)
        """
        offset_constraint_values = step_horizon * self._controller.number_of_general_constraints
        for i in range(0, self._controller.number_of_general_constraints):
            cost = self._controller.general_constraints[i].evaluate_cost(state, input)
            constraint_values[offset_constraint_values + i, 0] = cost

        return constraint_values

    def generate_cost_function(self):
        """ 
        Generate Casadi code of cost and gradient function: 
                - c-code
                - Casadi functions
        """
        initial_state = cd.SX.sym('initial_state', self._controller.model.number_of_states, 1)
        state_reference = cd.SX.sym('state_reference', self._controller.model.number_of_states, 1)
        input_reference = cd.SX.sym('input_reference', self._controller.model.number_of_inputs, 1)

        lambdas = cd.SX.sym('lambdas', self._controller.number_of_general_constraints * self._controller.horizon, 1)
        general_constraint_weights = cd.SX.sym('general_constraint_weights',self._controller.number_of_general_constraints * self._controller.horizon,1)

        static_casadi_parameters = cd.vertcat(initial_state, state_reference,input_reference,lambdas,general_constraint_weights)

        constraint_weights = cd.SX.sym('constraint_weights', self._controller.number_of_constraints, 1)
        
        input_all_steps = cd.SX.sym('input_all_steps', self._controller.model.number_of_inputs*self._controller.horizon, 1)
        cost=cd.SX.sym('cost',1,1)
        cost=0

        current_state=initial_state
        for i in range(1,self._controller.horizon+1):
            input = input_all_steps[(i-1)*self._controller.model.number_of_inputs:i*self._controller.model.number_of_inputs]
            current_state = self._controller.model.get_next_state(current_state,input)

            cost = cost + self._controller.stage_cost(current_state,input,i,state_reference,input_reference)
            cost = cost + self._controller.generate_cost_constraints(current_state,input,constraint_weights)

            # Extra terms associated with the lagrangian - lambda * c(x) + mu * c(c) ^ 2
            step_horizon = i - 1
            general_constraints_cost = self.generate_cost_general_constraints(current_state, input, lambdas, general_constraint_weights, step_horizon)
            cost = cost + general_constraints_cost

        (cost_function, cost_function_derivative_combined) = \
            ccg.setup_casadi_functions_and_generate_c(static_casadi_parameters,input_all_steps,constraint_weights,cost,\
                                                      self._controller.location)

        # generate the general constraints functions
        state = cd.SX.sym('state', self._controller.model.number_of_states, 1)
        constraint_values = cd.SX.sym('constraint_values',self._controller.number_of_general_constraints * self._controller.horizon, 1)

        state = initial_state
        for i in range(0, self._controller.horizon):
            input = input_all_steps[i * self._controller.model.number_of_inputs:(i+1) * self._controller.model.number_of_inputs]

            state = self._controller.model.get_next_state(state, input)

            constraint_values = self.evaluate_constraints(state, input,constraint_values, i)

        ccg.generate_c_constraints(initial_state, input_all_steps, constraint_values, self._controller.location)

        return (cost_function,cost_function_derivative_combined)

    @property
    def dimension(self):
        return self._dimension