classdef Nonconvex_constraints < nmpccodegen.controller.obstacles.Obstacle
    %NON_CONVEX_CONSTRAINTS obstacle excisting of non convex
    %constrains
    %   This obstacle allows the users to easily find a custom object.
    
    properties(Access = private)
        constraints
    end
    methods
        function obj = Nonconvex_constraints(model)
            % - model = Model of the controlled system.
            obj@nmpccodegen.controller.obstacles.Obstacle(model)
            obj.constraints={};
        end
        function obj = add_constraint(obj,constraint)
            % Add an nonconvex constraint.
            %   constraint = Matlab function.
            
            number_of_constraints = obj.get_number_of_constraints();
            if(number_of_constraints==0)
                obj.constraints ={constraint};
            else
                obj.constraints{end+1} = constraint;
            end
        end
        function number_of_constraints = get_number_of_constraints(obj)
            % Get the number of nonconvex constraints.
            number_of_constraints = length(obj.constraints);
        end
        function value =  evaluate_coordinate_state_cost(obj,coordinates_state)
            value = 0;
            % if there actually are constraints
            if (obj.get_number_of_constraints() ~= 0)
                value=1;
                for i=1:obj.get_number_of_constraints()
                    h = obj.constraints{i};
                    value = value*nmpccodegen.controller.obstacles.Obstacle.trim( ...
                        h(coordinates_state)...
                        );
                end
            end
        end
    end
end

