function [ prox_g_x ] = prox_g_1( x,w )
   if(norm(x,1)<w)
       prox_g_x = x;
   elseif(norm(x,1)>2*w)
       prox_g_x = sign(x)*(norm(x,1)-w);
   else
       prox_g_x = sign(x)*w;
   end
end

