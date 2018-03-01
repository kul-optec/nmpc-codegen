classdef Single_shot_definition
    %SINGLE_SHOT_DEFINITION Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        controller
        dimension
    end
    
    methods
        function obj = Single_shot_definition(controller)
            obj.controller = controller;
            obj.dimension = dimension;
        end
        function [cost_function,cost_function_derivative_combined] = generate_cost_function(obj)
            initial_state = casadi.SX.sym('initial_state', obj.controller.model.number_of_states, 1);
            state_reference = casadi.SX.sym('state_reference', obj.controller.model.number_of_states, 1);
            input_reference = casadi.SX.sym('input_reference', obj.controller.model.number_of_inputs, 1);
            static_casadi_parameters = vertcat(initial_state, state_reference,input_reference);

            obstacle_weights = casadi.SX.sym('obstacle_weights', obj.controller.number_of_obstacles, 1);
        
            input_all_steps = casadi.SX.sym('input_all_steps', obj.controller.model.number_of_inputs*obj.controller.horizon, 1);
%             cost=casadi.SX.sym('cost',1,1);% TODO, check if this is really needed.       

            cost=0;
            current_state=initial_state;
            for i=1:obj.controller.horizon+1
                input = input_all_steps(...
                    (i-1)*obj.controller.model.number_of_inputs+1:...
                    i*obj.controller.model.number_of_inputs);
                
                current_state = obj.controller.model.get_next_state(current_state,input);

                cost = cost + obj.controller.calculate_stage_cost(current_state,input,i,state_reference,input_reference);
                cost = cost + obj.controller.generate_cost_obstacles(current_state,obstacle_weights);
            end
            [cost_function, cost_function_derivative_combined] = ...
                Casadi_code_generator.setup_casadi_functions_and_generate_c(...
                    static_casadi_parameters,input_all_steps,obstacle_weights,cost, ...
                    obj.controller.location);
        end
        
    end
    
end

