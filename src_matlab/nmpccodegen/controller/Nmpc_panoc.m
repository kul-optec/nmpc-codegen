classdef Nmpc_panoc
    %NMPC_PANOC Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        location_lib
        model
        dimension_panoc=0;
        stage_cost
        terminal_cost
        horizon=10
        shooting_mode = 'single shot' 
        lbgfs_buffer_size
        data_type = 'double precision'
        panoc_max_steps=20
        panoc_min_steps=0
        min_residual=-3
        integrator_casadi=false
        pure_prox_gradient=false
        globals_generator
        obstacles=[];
        cost_function
        cost_function_derivative_combined
    end
    
    methods
        function obj = Nmpc_panoc( location_lib,model,stage_cost,terminal_cost)
            obj.location_lib=location_lib;
            obj.model=model;
            obj.stage_cost=stage_cost;
            if (nargin == 3)
                obj.terminal_cost=[];
            elseif (nargin == 4)
                obj.terminal_cost=terminal_cost;
            else
                disp('error invalid amount of parameters in nmpc_constructor')
            end
            obj.globals_generator = Globals_generator([location_lib '/globals/globals_dyn.h']);
        end
        function number_of_obstacles = get_number_of_obstacles(obj)
            number_of_obstacles = length(obj.obstacles);
        end
        function generate_code(obj)
            % start with generating the cost function
            if(strcmp(obj.shooting_mode,'single shot'))
                self.generate_cost_function_singleshot()
            elseif(strcmp(obj.shooting_mode,'multiple shot'))
                obj.generate_cost_function_multipleshot()
            else
                disp('ERROR in generating code: invalid choice of shooting mode [single shot|multiple shot]')
            end

            % obj.globals_generator.generate_globals(obj)

            % optional feature, a c version of the integrator
            % if(obj.integrator_casadi)
            %     obj.generate_integrator()
            % end

            % obj.model.generate_constraint(obj.location_lib)
            
        end

        function obj=generate_cost_function_singleshot(obj)
            ssd = Single_shot_definition(obj);
            [cost_function_, cost_function_derivative_combined_] = ssd.generate_cost_function();

            obj.cost_function = cost_function_;
            obj.cost_function_derivative_combined=cost_function_derivative_combined_;
            obj.dimension_panoc=ssd.dimension;
        end
        function generate_cost_function_multipleshot(obj)
        end
        function generate_integrator(obj)
        end
    end
    
end

