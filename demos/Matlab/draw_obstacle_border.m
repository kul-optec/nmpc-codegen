function draw_obstacle_border( h,xlim,number_of_points )
%DRAW_OBSTACLE_BORDER Summary of this function goes here
%   Detailed explanation goes here
    x = linspace(xlim(1),xlim(2),number_of_points);
    y = zeros(number_of_points,1);

    for i=1:number_of_points
        y(i)=h(x(i));
    end

    plot(x,y)

end

