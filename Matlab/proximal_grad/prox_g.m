function [ prox_g_x ] = prox_g( x,w,dimension )
    prox_g_x=zeros(dimension,1);
    for i=1:dimension
       if(abs(x(i))<w)
           prox_g_x(i) = x(i);
       elseif(abs(x)>2*w)
           prox_g_x(i) = sign(x(i))*(abs(x(i))-w);
       else
           prox_g_x(i) = sign(x(i))*(abs(x(i)-w));
       end
    end
end

