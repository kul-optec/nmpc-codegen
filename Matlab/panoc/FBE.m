function [ FBE_x] = FBE( x,gamma,beta,f,df,proxg )
    x_new = proxg( x-df(x)*gamma );
    FBE_x = f(x) - dot(df(x),x_new-x)+ ...
        ((1-beta)/(2*gamma))*norm(x_new-x,2);
end