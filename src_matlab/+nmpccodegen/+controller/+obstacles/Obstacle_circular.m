classdef Obstacle_circular < nmpccodegen.controller.obstacles.Obstacle
    %RECTANGLE Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        center_coordinates
        radius
    end
    
    methods
        function obj = Obstacle_circular(center_coordinates,radius)
            obj.center_coordinates=center_coordinates;
            obj.radius=radius;
        end
        function cost = evaluate_cost(obj,coordinates_state)
            cost = nmpccodegen.controller.obstacles.Obstacle.trim_and_square(obj.radius ...
                    - sqrt(sum1((obj.center_coordinates-coordinates_state).^2))...
                    );
        end
    end
    
end