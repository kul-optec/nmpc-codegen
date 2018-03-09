classdef Obstacle_nonconvex_constraints < nmpccodegen.controller.obstacles.Obstacle
    %OBSTACLE_NON_CONVEX_CONSTRAINTS obstacle excisting of non convex
    %constrains
    %   Detailed explanation goes here
    
    properties(Access = private)
        constraints
    end
    methods
        function obj = Obstacle_nonconvex_constraints()
            obj.constraints=[];
        end
        function obj = add_constraint(obj,constraint)
            obj.constraints = [obj.constraints constraint];
        end
        function number_of_constraints = get_number_of_constraints(obj)
            number_of_constraints = length(obj.constraints);
        end
        function value =  evaluate_cost(obj,coordinates_state)
            value = 0;
            % if there actually are constraints
            if (obj.get_number_of_constraints() ~= 0)
                value=1;
                for i=1:obj.get_number_of_constraints()
                    h = obj.constraints(i);
                    value = value*Obstacle.trim_and_square( ...
                        h(coordinates_state)...
                        );
                end
            end
        end
    end
end

