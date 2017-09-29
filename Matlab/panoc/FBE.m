function [ FBE_x] = FBE( x,gamma,beta,f,df,g,proxg )
    x_new = proxg( x-df(x)*gamma );
    FBE_x = f(x) + g(x_new) - dot(df(x),x-x_new)+ ...
        ((1-beta)/(2*gamma))*norm(x-x_new,2)^2;
end