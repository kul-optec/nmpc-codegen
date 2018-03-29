classdef Obstacle_circular < nmpccodegen.controller.obstacles.Obstacle
    %RECTANGLE A circular object.
    %   A simple two-dimensional circular object.
    
    properties
        center_coordinates % The center coordinates of the circle
        radius % The radius of the circle.
    end
    
    methods
        function obj = Obstacle_circular(center_coordinates,radius)
            % center_coordinates = The center coordinates of the circle
            % radius = The radius of the circle.
            obj.center_coordinates=center_coordinates;
            obj.radius=radius;
        end
        function cost = evaluate_cost(obj,coordinates_state)
            % Evaluate the costs of the obstacle at a particular state.
            cost = nmpccodegen.controller.obstacles.Obstacle.trim(obj.radius ...
                    - sqrt(sum1((obj.center_coordinates-coordinates_state).^2))...
                    );
        end
        function plot(obj)
            % Plot the obstacle on the active figure
            angles = 0:0.01:2*pi;
            plot(obj.radius * cos(angles) + obj.center_coordinates(1), ...
                obj.radius * sin(angles) + obj.center_coordinates(2), 'linewidth', 2, ...
                'Color', 'black');
        end
        
    end
    
end