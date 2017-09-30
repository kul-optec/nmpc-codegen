function [ g_x ] = g_2( x )
    % indicator function of {-1;0;1}
    if(x==1 || x==0 || x==-1 )
        g_x=0;
    else 
        g_x=10^10;
    end
end

