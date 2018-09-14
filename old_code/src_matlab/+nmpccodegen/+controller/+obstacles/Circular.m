classdef Circular < nmpccodegen.controller.obstacles.Obstacle
    %RECTANGLE A circular object.
    %   A simple two-dimensional circular object.
    
    properties
        center_coordinates % The center coordinates of the circle
        radius % The radius of the circle.
    end
    
    methods
        function obj = Circular(center_coordinates,radius,model)
            % - center_coordinates : The center coordinates of the circle
            % - radius : The radius of the circle.
            % - model : Model of the controlled system.
            obj@nmpccodegen.controller.obstacles.Obstacle(model)
            
            obj.center_coordinates=center_coordinates;
            obj.radius=radius;
        end
        function cost = evaluate_coordinate_state_cost(obj,coordinates_state)
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
        function plot3(obj)
            % create sphere around orgin with radius one
            [x,y,z] = sphere;
            
            % amplify the radius
            x=x.*obj.radius;
            y=y.*obj.radius;
            z=z.*obj.radius;
            
            % shift the center
            x=x+obj.center_coordinates(1);
            y=y+obj.center_coordinates(2);
            z=z+obj.center_coordinates(3);
            
            surf(x,y,z);
        end
    end
    
end