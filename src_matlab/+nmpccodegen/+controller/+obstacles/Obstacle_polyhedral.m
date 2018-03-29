classdef Obstacle_polyhedral < nmpccodegen.controller.obstacles.Obstacle
    %POLYHEDRAL A simple polyhedral obstacles
    %   construct obstacle of form a[i,:]^Tb +b , for all i
    
    properties
        a % The matrix a of a[i,:]^Tb +b , for all i
        b % The matrix b of a[i,:]^Tb +b , for all i
        number_of_constraints 
        dimension % The dimension of the polyhedral derived from the matrix a.
    end
    
    methods
        function obj = Obstacle_polyhedral(a,b)
            % a = The matrix a of a[i,:]^Tb +b , for all i
            % b = The matrix b of a[i,:]^Tb +b , for all i
            
            obj.a=a;
            obj.b=b;
            
            [dimension,number_of_constraints] = size(a);
            
            obj.dimension = dimension;
            obj.number_of_constraints = number_of_constraints;
        end
        function value = evaluate_cost(obj,coordinates_state)
            % Evaluate the cost of the obstacle at a particular state.
            value=1.;
            for i=1:obj.number_of_constraints
                value = value * nmpccodegen.controller.obstacles.Obstacle.trim(...
                    (obj.a(:,i)'*coordinates_state)+ obj.b(i)...
                );
            end
        end
    end
    
end

