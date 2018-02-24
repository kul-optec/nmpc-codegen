% where myfun is a MATLAB function such as:
% function [f,g] = myfun(x)
% f = sum(sin(x) + 3);
% if ( nargout > 1 ), g = cos(x); end

function [f,g] = myfun_poly(x)
    f =x(1)^10 + x(2)^10;
    g = [10*x(1)^9; 10*x(2)^9 ];
end