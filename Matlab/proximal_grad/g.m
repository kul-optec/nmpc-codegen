function [ g_x ] = g( x,w )
    g_x = max(abs(x)-w,0);
end

