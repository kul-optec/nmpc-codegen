classdef Single_shot_definition
    %SINGLE_SHOT_DEFINITION The single shot cost function used by
    %nmpc_controller
    %   This internal class is used by nmpc_controller to generate the 
    %   casadi cost function of the single shot definition. And calls the
    %   Globals_generator class to generate the c-file.
    
    properties
        controller % nmpc_controller object provided by the construct.
        dimension % Dimension of the optimization problem, calculated by the constructor.
    end
    
    methods
        function obj = Single_shot_definition(controller)
            % Constructor single shot definition
            %   -controller : nmpc_controller object
            obj.controller = controller;
            obj.dimension = controller.model.number_of_inputs*controller.horizon;
        end
        function [cost_function,cost_function_derivative_combined] = generate_cost_function(obj)
            % Generate the casdi cost function and calls the 
            % Globals_generator class to generate the c-file.
            initial_state = casadi.SX.sym('initial_state', obj.controller.model.number_of_states, 1);
            state_reference = casadi.SX.sym('state_reference', obj.controller.model.number_of_states, 1);
            input_reference = casadi.SX.sym('input_reference', obj.controller.model.number_of_inputs, 1);
            static_casadi_parameters = vertcat(initial_state, state_reference,input_reference);

            constraint_weights = casadi.SX.sym('constraint_weights', obj.controller.number_of_constraints, 1);
        
            input_all_steps = casadi.SX.sym('input_all_steps', obj.controller.model.number_of_inputs*obj.controller.horizon, 1);     

            cost=0;
            current_state=initial_state;
            for i=1:obj.controller.horizon
                input = input_all_steps(...
                    (i-1)*obj.controller.model.number_of_inputs+1:...
                    i*obj.controller.model.number_of_inputs);
                
                current_state = obj.controller.model.get_next_state(current_state,input);

                cost = cost + obj.controller.calculate_stage_cost(current_state,input,i,state_reference,input_reference);
                cost = cost + obj.controller.generate_cost_constraints(current_state,input,constraint_weights);
            end
            [cost_function, cost_function_derivative_combined] = ...
                nmpccodegen.controller.Casadi_code_generator.setup_casadi_functions_and_generate_c(...
                    static_casadi_parameters,input_all_steps,constraint_weights,cost, ...
                    obj.controller.location);
        end
        
    end
    
end

