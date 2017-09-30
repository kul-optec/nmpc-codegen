function [ prox_g_x ] = prox_g_2( x )
if(x<-0.5)
    prox_g_x=-1;
elseif(x>0.5)
    prox_g_x=1;
else
    prox_g_x=0;
end

