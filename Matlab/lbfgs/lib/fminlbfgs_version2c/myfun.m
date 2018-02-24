% where myfun is a MATLAB function such as:
% function [f,g] = myfun(x)
% f = sum(sin(x) + 3);
% if ( nargout > 1 ), g = cos(x); end

function [f,g] = myfun(x)
    a=1;
    b=100;
    f =(a-x(1))^2 + b*(x(2)-x(1))^2;
    g = [-2*(a-(b+1)*x(1)+b*x(2)); 2*b*(x(2)-x(1)) ];
end