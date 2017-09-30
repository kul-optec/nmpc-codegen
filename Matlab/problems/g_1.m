function [ g_x ] = g_1( x,w )
    g_x = max(norm(x,1)-w,0);
end

