classdef Obstacle < matlab.mixin.Heterogeneous
    %OBSTACLE Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
    end
    
    methods(Abstract)
        evaluate_cost(obj,coordinates_state);
    end
    methods(Static)
        function tqs_x = trim_and_square(x)
            tqs_x = max(x,0)^2;
        end
    end
end

