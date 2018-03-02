classdef Model_continuous < nmpccodegen.models.Model
    %MODEL_CONTINIOUS  a discrete model describing the system behavior
    %   Detailed explanation goes here
    properties
        integrator
    end
    
    methods
        function obj = Model_continuous(system_equations,input_constraint,step_size,...
                number_of_states,number_of_inputs,indices_coordinates,integrator)
            obj = obj@nmpccodegen.models.Model(system_equations,input_constraint,step_size,...
                number_of_states,number_of_inputs,indices_coordinates);
            obj.integrator = integrator;
            
        end
        function next_state = get_next_state(obj,state,input)
            % define the discrete system equations
            function_system = @(x) obj.system_equations(x,input);
            discrete_system_equations = @(discrete_state) ...
                nmpccodegen.models.integrate( ...
                    discrete_state,obj.step_size, ...
                    function_system,obj.integrator);
            
            % get next state of discrete system
            next_state = discrete_system_equations(state);
        end
    end
    
end