classdef Single_shot_LA_definition
    %SINGLE_SHOT_DEFINITION Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        controller
        dimension
    end
    
    methods
        function obj = Single_shot_LA_definition(controller)
            obj.controller = controller;
            obj.dimension = controller.model.number_of_inputs*controller.horizon;
        end
        function cost = generate_cost_obstacles_lambdas(obj,current_state,lambdas)
            cost=0;
            for i=1:obj.controller.number_of_obstacles
                cost = cost + obj.controller.obstacles(i).evaluate_cost(current_state(obj.controller.model.indices_coordinates))*lambdas(i);
            end
        end
        function constraint_values = evaluate_constraints(obj,state,constraint_values,iteration_horizon)
            for i=1:obj.controller.number_of_obstacles
                if(iteration_horizon==1) 
                     constraint_values(i,1) = obj.controller.obstacles(i).evaluate_cost(state(obj.controller.model.indices_coordinates));
                else
                     constraint_values(i,1) = constraint_values(i,1) + obj.controller.obstacles(i).evaluate_cost(state(obj.controller.model.indices_coordinates));
                end
            end
        end
        function [cost_function,cost_function_derivative_combined] = generate_cost_function(obj)
            initial_state = casadi.SX.sym('initial_state', obj.controller.model.number_of_states, 1);
            
            state_reference = casadi.SX.sym('state_reference', obj.controller.model.number_of_states, 1);
            input_reference = casadi.SX.sym('input_reference', obj.controller.model.number_of_inputs, 1);
            lambdas = casadi.SX.sym('lambdas',  obj.controller.number_of_obstacles, 1);
            static_casadi_parameters = vertcat(initial_state, state_reference,input_reference,lambdas);

            obstacle_weights = casadi.SX.sym('obstacle_weights', obj.controller.number_of_obstacles, 1);
        
            input_all_steps = casadi.SX.sym('input_all_steps', obj.controller.model.number_of_inputs*obj.controller.horizon, 1);

            cost=0;
            current_state=initial_state;
            for i=1:obj.controller.horizon
                input = input_all_steps(...
                    (i-1)*obj.controller.model.number_of_inputs+1:...
                    i*obj.controller.model.number_of_inputs);
                
                current_state = obj.controller.model.get_next_state(current_state,input);

                cost = cost + obj.controller.calculate_stage_cost(current_state,input,i,state_reference,input_reference);
                cost = cost + obj.controller.generate_cost_obstacles(current_state,obstacle_weights);
                cost = cost + obj.generate_cost_obstacles_lambdas(current_state,lambdas);
            end
            [cost_function, cost_function_derivative_combined] = ...
                nmpccodegen.controller.Casadi_code_generator.setup_casadi_functions_and_generate_c(...
                    static_casadi_parameters,input_all_steps,obstacle_weights,cost, ...
                    obj.controller.location);
            
            state = casadi.SX.sym('state', obj.controller.model.number_of_states, 1);
            constraint_values = casadi.SX.sym('constraint_values',obj.controller.number_of_obstacles, 1);
            
            state = initial_state;
            for i=1:obj.controller.horizon
                input = input_all_steps(...
                    (i-1)*obj.controller.model.number_of_inputs+1:...
                    i*obj.controller.model.number_of_inputs);
                
                obj.evaluate_constraints(state,constraint_values,i);
                state = obj.controller.model.get_next_state(state,input);
            end
            
            nmpccodegen.controller.Casadi_code_generator.generate_c_constraints(...
                initial_state,input_all_steps,constraint_values,obj.controller.location);
        end
        
    end
    
end

