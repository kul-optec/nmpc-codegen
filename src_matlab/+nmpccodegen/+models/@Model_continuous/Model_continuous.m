classdef Model_continuous < nmpccodegen.models.Model
    %MODEL_CONTINUOUS  A contious discretized model describing the system behavior
    %   - The same as a model, but the user provides a continue model and
    %   the name of an integrator
    properties
        integrator % string that contains the name of the integrator, all the names are found in the user manual
    end
    
    methods
        function obj = Model_continuous(system_equations,input_constraint,step_size,...
                number_of_states,number_of_inputs,indices_coordinates,integrator)
            % Constructor of a continuous Model
            %   - system_equations: The system equations, expressed as Matlab
            %   functions in the form f(state,input).
            %   - input_constraint: The input constraints, must be a nmpccodegen.Cfunctions.ProximalFunction object.
            %   - step_size: The step size of the indicator.
            %   - number_of_states: The dimension of the state.
            %   - number_of_inputs: The dimension of the input.
            %   - indices_coordinates: 
            %   - integrator: A string that contains the name of the integrator, all the names are found in the user manual
            obj = obj@nmpccodegen.models.Model(system_equations,input_constraint,step_size,...
                number_of_states,number_of_inputs,indices_coordinates);
            obj.integrator = integrator;
            
        end
        function next_state = get_next_state(obj,state,input)
            % Get the next state of the system using the input and the
            % current state.
            
            % define the discrete system equations
            function_system = @(x) obj.system_equations(x,input);
            discrete_system_equations = @(discrete_state) ...
                nmpccodegen.models.integrate( ...
                    discrete_state,obj.step_size, ...
                    function_system,obj.integrator);
            
            % get next state of discrete system
            next_state = discrete_system_equations(state);
        end
        function next_state = get_next_state_double(obj,state,input)
            % Get the next state of the system using the input and the
            % current state in doubles and not in casadi variables.
            
            next_state_casadi = get_next_state(obj,state,input);
            next_state = double(full(next_state_casadi(1).evalf));
        end
    end
    
end