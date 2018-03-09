classdef Obstacle_rectangular < nmpccodegen.controller.obstacles.Obstacle
    %RECTANGLE Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        width
        height
        center_coordinates
    end
    
    methods
        function obj = Obstacle_rectangular(center_coordinates,width,height)
            obj.center_coordinates=center_coordinates;
            obj.width=width;
            obj.height=height;
        end
        function cost = evaluate_cost(obj,coordinates_state)
            [x_up,x_down,y_up,y_down] = get_corner_coordinates(obj);
            a = ([-1. 0.; 1., 0. ;0., -1.; 0., 1.])';
            b = [x_up; -x_down; y_up; -y_down];
            
            cost =  nmpccodegen.controller.obstacles.Obstacle_polyhedral(a, b).evaluate_cost(coordinates_state);
        end
        function plot(obj)
            [x_up,x_down,y_up,y_down] = get_corner_coordinates(obj);
            plot([x_down x_up],[y_down y_down],'linewidth', 2,'Color', 'black');
            plot([x_down x_up],[y_up y_up],'linewidth', 2,'Color', 'black');
            plot([x_up x_up],[y_up y_down],'linewidth', 2,'Color', 'black');
            plot([x_down x_down],[y_down y_up],'linewidth', 2,'Color', 'black');
            plot(y_up)
        end
        function [x_up,x_down,y_up,y_down] = get_corner_coordinates(obj)
            x_up = obj.center_coordinates(1) + obj.width / 2;
            x_down = obj.center_coordinates(1) - obj.width / 2;
            y_up = obj.center_coordinates(2) + obj.height / 2;
            y_down = obj.center_coordinates(2) - obj.height / 2;
        end
    end
    
end

