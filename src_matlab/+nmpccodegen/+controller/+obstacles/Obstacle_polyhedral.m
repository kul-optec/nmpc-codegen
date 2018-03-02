classdef Obstacle_polyhedral < nmpccodegen.controller.Obstacle
    %POLYHEDRAL Summary of this class goes here
    %   construct obstacle of form a[i,:]^Tb +b , for all i
    
    properties
        a
        b
        number_of_constraints
        dimension
    end
    
    methods
        function obj = Obstacle_polyhedral(a,b)
            obj.a=a;
            obj.b=b;
            
            [dimension,number_of_constraints] = size(a);
            
            obj.dimension = dimension;
            obj.number_of_constraints = number_of_constraints;
        end
        function value = evaluate_cost(obj,coordinates_state)
            value=1.;
            for i=1:obj.number_of_constraints
                value = value * Obstacle.trim_and_square(...
                    (obj.a(:,i)'*coordinates_state)+ obj.b(i)...
                );
            end
        end
    end
    
end

