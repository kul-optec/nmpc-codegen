classdef Constraint < matlab.mixin.Heterogeneous
    %OBSTACLE Abstract class that represents the minimum interface of an
    %general constraint
    %   An constraint needs at least the following interface:
    %       - evaluate_cost , evaluates the cost of the constraint
    properties
    end
    
    methods(Abstract)
        evaluate_cost(obj,state,input);
    end
end

