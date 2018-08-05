classdef Rectangular < nmpccodegen.controller.obstacles.Obstacle
    %RECTANGULAR A simple rectangular obstacle.
    %  A simple two-dimensional rectangular obstacle.
    
    properties
        width % The width of the rectangular.
        height % The height of the rectangular.
        center_coordinates % The center coordinates of the rectangular.
    end
    
    methods
        function obj = Rectangular(center_coordinates,width,height,model)
            % - width = The width of the rectangular.
            % - height = The height of the rectangular.
            % - center_coordinates = The center coordinates of the rectangular.
            % - model = Model of the controlled system.
            obj@nmpccodegen.controller.obstacles.Obstacle(model)
            obj.center_coordinates=center_coordinates;
            obj.width=width;
            obj.height=height;
        end
        function cost = evaluate_coordinate_state_cost(obj,coordinates_state)
            % Evaluate the cost of the obstacle at a particular location.
            [x_up,x_down,y_up,y_down] = get_corner_coordinates(obj);
            a = ([-1. 0.; 1., 0. ;0., -1.; 0., 1.])';
            b = [x_up; -x_down; y_up; -y_down];
            
            cost =  nmpccodegen.controller.obstacles.Polyhedral(a, b, obj.model).evaluate_coordinate_state_cost(coordinates_state);
        end
        function plot(obj)
            % Plots the rectangular obstacle to the active figure.
            [x_up,x_down,y_up,y_down] = get_corner_coordinates(obj);
            plot([x_down x_up],[y_down y_down],'linewidth', 2,'Color', 'black');
            plot([x_down x_up],[y_up y_up],'linewidth', 2,'Color', 'black');
            plot([x_up x_up],[y_up y_down],'linewidth', 2,'Color', 'black');
            plot([x_down x_down],[y_down y_up],'linewidth', 2,'Color', 'black');
            plot(y_up)
        end
    end
    methods (Access = private)
        function [x_up,x_down,y_up,y_down] = get_corner_coordinates(obj)
            % Internal function used to get the coordinates of the corners
            % of the rectangular.
            x_up = obj.center_coordinates(1) + obj.width / 2;
            x_down = obj.center_coordinates(1) - obj.width / 2;
            y_up = obj.center_coordinates(2) + obj.height / 2;
            y_down = obj.center_coordinates(2) - obj.height / 2;
        end
    end
    
end

