classdef Input_norm < nmpccodegen.controller.constraints.Constraint
    %INPUT_NORM Constraint that punishes if the 2-norm of the input is too
    %high    
    properties
        max_norm
    end
    
    methods
        function obj = Input_norm(max_norm)
            obj.max_norm=max_norm;
        end
        function cost = evaluate_cost(obj,state,input)
            % evaluate the cost for a specific state and input
            %   -state : array of size (n,1) that represents state
            %   -input : array of size (n,1) that represents input
            norm_input = sum1(input.^2);
            cost = max(norm_input - obj.max_norm^2,0)^2; % if norm is higer then max_norm return penalty
        end        
    end
    
end