classdef Obstacle < nmpccodegen.controller.constraints.Constraint
    %OBSTACLE Abstract class that represents the minimum interface of an
    %obstacle. It is a special case of a constraint, as only certain states
    %will be used.
    %   An obstacle needs at least the following interface:
    %       - evaluate_cost , evaluates the cost of the soft constraint
    
    properties
        model
    end
    
    methods(Abstract)
        evaluate_coordinate_state_cost(obj,coordinates_state);
    end
    methods
        function obj = Obstacle(model)
            obj.model=model;
        end
        function cost = evaluate_cost(obj,state,input)
            cost = obj.evaluate_coordinate_state_cost( ...
                state(obj.model.indices_coordinates));
        end
    end
    methods(Static)
        function tqs_x = trim(x)
            % Used internally by all the obstacles to trim the cost,  as in
            % make the cost only positive.
            tqs_x = max(x,0);
        end
    end
end

