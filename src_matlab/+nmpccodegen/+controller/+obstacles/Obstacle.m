classdef Obstacle < matlab.mixin.Heterogeneous
    %OBSTACLE Abstract class that represents the minimum interface of an
    %obstacle
    %   An obstacle needs at least the following interface:
    %       - evaluate_cost , evaluates the cost of the soft constraint
    
    properties
    end
    
    methods(Abstract)
        evaluate_cost(obj,coordinates_state);
    end
    methods(Static)
        function tqs_x = trim(x)
            % Used internally by all the obstacles to trim the cost,  as in
            % make the cost only positive.
            tqs_x = max(x,0);
        end
    end
end

