classdef Single_shot_definition
    %SINGLE_SHOT_DEFINITION Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        controller
        dimension
    end
    
    methods
        function obj = Single_shot_definition(controller)
            obj.controller = controller;
            obj.dimension = dimension;
        end
        function [cost_function,cost_function_derivative_combined] = generate_cost_function(obj)
            cost_function=0;
            cost_function_derivative_combined=0;
        end
        
    end
    
end

