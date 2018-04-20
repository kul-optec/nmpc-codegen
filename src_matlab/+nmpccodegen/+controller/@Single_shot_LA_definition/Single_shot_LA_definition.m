classdef Single_shot_LA_definition
    %SINGLE_SHOT_LA_DEFINITION Definition of single shot MPC problem with
    %Lagrangian
    %   This internal class is used by nmpc_controller to generate the 
    %   casadi cost function of the single shot definition with Lagrangian. 
    %   And calls the Globals_generator class to generate the c-file.
    %   The Lagrangian is used when there are general constraints.
    
    properties
        controller
        dimension
    end
    methods(Access =  private)
        function cost = generate_cost_general_constraints(obj,current_state,input,lambdas,general_constraint_weights,step_horizon)
            % Evaluate function cost of all general constraints for 1 step in the horizon
            %   L = lambda ci(x) + mu ci(x)^2
            %       current_state: state of this step in the horizon
            %       input: current inpu applied to the systen
            %       lambdas: lambda's for this step of the horizon
            %       general_constraint_weights: mu's for this step of the horizon
            %       step_horizon: the index of the step in the horizon (the first step is index 1)
            number_of_general_constraints = length(obj.controller.general_constraints);
            offset_constraints = (step_horizon-1)*number_of_general_constraints;
            cost=casadi.SX(1,1);
            for i=1:number_of_general_constraints
                constraint_cost = obj.controller.general_constraints(i).evaluate_cost(current_state,input);
                cost = cost - constraint_cost*lambdas(offset_constraints+i);
                cost = cost + (constraint_cost^2)*general_constraint_weights(offset_constraints+i);
            end
        end
        function constraint_values = evaluate_constraints(obj,state,input,constraint_values,step_horizon)
            % Evaluate cost of general constraints for 1 step in the horizon
            %       state: state of this step in the horizon
            %       input: current inpu applied to the systen
            %       constraint_values: contains the costs of the constraints
            %       step_horizon: the index of the step in the horizon (the first step is index 1)
            number_of_general_constraints = length(obj.controller.general_constraints);
            offset_constraint_values = (step_horizon-1)*number_of_general_constraints;
            for i=1:number_of_general_constraints
                cost = obj.controller.general_constraints(i).evaluate_cost(state,input);
                constraint_values(offset_constraint_values+i,1) = cost;
            end
        end
    end
    methods(Access =  public)
        function obj = Single_shot_LA_definition(controller)
            % Constructor single shot definition
            %   Saves the controller and calculates the dimension of the
            %   optimization problem.
            %       controller = nmpc_controller object
            obj.controller = controller;
            obj.dimension = controller.model.number_of_inputs*controller.horizon;
        end
        
        function [cost_function,cost_function_derivative_combined] = generate_cost_function(obj)
            % generate the cost function and general constraints function using casadi
            initial_state = casadi.SX.sym('initial_state', obj.controller.model.number_of_states, 1);
            state_reference = casadi.SX.sym('state_reference', obj.controller.model.number_of_states, 1);
            input_reference = casadi.SX.sym('input_reference', obj.controller.model.number_of_inputs, 1);
            
            lambdas = casadi.SX.sym('lambdas',length(obj.controller.general_constraints)*obj.controller.horizon, 1);
            general_constraint_weights = casadi.SX.sym('general_constraint_weights',length(obj.controller.general_constraints)*obj.controller.horizon, 1);
            
            static_casadi_parameters = vertcat(initial_state, state_reference,input_reference,...
                lambdas,general_constraint_weights);

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
                
                % Extra terms associated with the lagrangian - lambda*c(x) + mu*c(c)^2
                general_constraints_cost = obj.generate_cost_general_constraints(...
                        current_state,input,lambdas,general_constraint_weights,i);
                cost = cost + general_constraints_cost;
            end
            [cost_function, cost_function_derivative_combined] = ...
                nmpccodegen.controller.Casadi_code_generator.setup_casadi_functions_and_generate_c(...
                    static_casadi_parameters,input_all_steps,constraint_weights,cost, ...
                    obj.controller.location);
            
            % generate the general constraints functions
            constraint_values = casadi.SX.sym('constraint_values',length(obj.controller.general_constraints)*obj.controller.horizon, 1);
            
            state = initial_state;
            for i=1:obj.controller.horizon
                input = input_all_steps(...
                    (i-1)*obj.controller.model.number_of_inputs+1:...
                    i*obj.controller.model.number_of_inputs);
                
                state = obj.controller.model.get_next_state(state,input);
                
                constraint_values = obj.evaluate_constraints(state,input,...
                    constraint_values,i);
            end
            
            nmpccodegen.controller.Casadi_code_generator.generate_c_constraints(...
                initial_state,input_all_steps,constraint_values,obj.controller.location);
        end
        
    end
    
end

