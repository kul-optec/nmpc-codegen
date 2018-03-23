classdef Nmpc_panoc
    %NMPC_PANOC Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        location
        model
        dimension_panoc=0;
        stage_cost
        terminal_cost
        horizon=10
        shooting_mode = 'single shot' 
        lbgfs_buffer_size = 50
        data_type = 'double precision'
        panoc_max_steps=20
        panoc_min_steps=0
        min_residual=-3
        integrator_casadi=false
        pure_prox_gradient=false
        globals_generator
        obstacles=[]
        number_of_obstacles=0
        general_constraints=[]
        cost_function
        cost_function_derivative_combined
    end
    
    methods
        function obj = Nmpc_panoc( location_lib,model,stage_cost,terminal_cost)
            obj.location=location_lib;
            obj.model=model;
            obj.stage_cost=stage_cost;
            if (nargin == 3)
                obj.terminal_cost=[];
            elseif (nargin == 4)
                obj.terminal_cost=terminal_cost;
            else
                disp('error invalid amount of parameters in nmpc_constructor')
            end
            obj.globals_generator = nmpccodegen.controller.Globals_generator([location_lib '/globals/globals_dyn.h']);
        end
        function obj=generate_code(obj)
            % start with generating the cost function
            if(strcmp(obj.shooting_mode,'single shot'))
                if(isempty(obj.general_constraints))
                    obj = obj.generate_cost_function_singleshot();
                else
                    obj = obj.generate_cost_function_singleshot_LA();
                end                
            elseif(strcmp(obj.shooting_mode,'multiple shot'))
                obj = obj.generate_cost_function_multipleshot();
            else
                disp('ERROR in generating code: invalid choice of shooting mode [single shot|multiple shot]');
            end

            obj.globals_generator.generate_globals(obj);

            % optional feature, a c version of the integrator
            if(obj.integrator_casadi)
                obj.generate_integrator();
            end

            obj.model.generate_constraint(obj.location)
            
        end

        function obj=generate_cost_function_singleshot(obj)
            ssd = nmpccodegen.controller.Single_shot_definition(obj);
            % generate the cost function in casadi syntax AND generate c
            % code in the background
            [cost_function_, cost_function_derivative_combined_] = ssd.generate_cost_function();

            obj.cost_function = cost_function_;
            obj.cost_function_derivative_combined=cost_function_derivative_combined_;
            obj.dimension_panoc=ssd.dimension;
        end
        function obj=generate_cost_function_singleshot_LA(obj)
            ssd = nmpccodegen.controller.Single_shot_LA_definition(obj);
            % generate the cost function in casadi syntax AND generate c
            % code in the background
            [cost_function_, cost_function_derivative_combined_] = ssd.generate_cost_function();

            obj.cost_function = cost_function_;
            obj.cost_function_derivative_combined=cost_function_derivative_combined_;
            obj.dimension_panoc=ssd.dimension;
        end
        function obj=generate_cost_function_multipleshot(obj)
            % TODO
            disp('Multiple shot is not implemented !');
        end
        function generate_integrator(obj)
            state = casadi.SX.sym('state', obj.model.number_of_states, 1);
            input = casadi.SX.sym('input', obj.model.number_of_inputs , 1);
            
            integrator = casadi.Function('integrator', {state, input}, {obj.model.get_next_state(state,input)});
            nmpccodegen.controller.Casadi_code_generator.translate_casadi_to_c(integrator,obj.location,'integrator');
        end
        function cost = calculate_stage_cost(obj,current_state,input,i,...
                                        state_reference,input_reference)
            if(i==obj.horizon)
                cost=obj.terminal_cost.evaluate_cost(current_state,input,i,state_reference,input_reference);
            else
                cost=obj.stage_cost.evaluate_cost(current_state,input,i,state_reference,input_reference);
            end
        end
        function obj = add_obstacle(obj,obstacle)
            obj.obstacles = horzcat(obj.obstacles,obstacle);
            obj.number_of_obstacles=length(obj.obstacles);
        end
        function obj = add_general_constraint(obj,general_constraint)
            obj.general_constraints = horzcat(obj.general_constraints,general_constraint);
        end
        function number_of_obstacles = get_number_of_obstacles(obj)
            number_of_obstacles = length(obj.obstacles);
        end
        function cost = generate_cost_obstacles(obj,state,obstacle_weights)
            if(obj.number_of_obstacles == 0)
                cost= 0.;
            else
                cost = 0.;
                for i=1:obj.number_of_obstacles
                    cost = cost + obstacle_weights(i)*...
                        (obj.obstacles(i).evaluate_cost(state(obj.model.indices_coordinates))).^2;
                end
            end
        end
    end
    
end

