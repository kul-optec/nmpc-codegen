classdef Obstacle_rectangular
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
            x_up = obj.center_coordinates(0) + obj.width / 2;
            x_down = obj.center_coordinates(0) - obj.width / 2;
            y_up = obj.center_coordinates(1) + obj.height / 2;
            y_down = obj.center_coordinates(1) - obj.height / 2;

            a = ([-1. 0.; 1., 0. ;0., -1.; 0., 1.])';
            b = [x_up; -x_down; y_up; -y_down];
            
            cost =  Obstacle_polyhedral(a, b).evaluate_cost(coordinates_state);
        end
    end
    
end

