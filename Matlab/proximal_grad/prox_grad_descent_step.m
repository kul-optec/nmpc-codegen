function [ x_new,gamma ] = prox_grad_descent_step( x,gamma,beta,proxg,f,df )    
    x_new = proxg(x-gamma*df(x));
    r=x_new-x;
    while(f(x_new)>f(x)- dot(df(x),x_new-x)+(1-beta)/(2*gamma) * norm(x_new-x,2))
        gamma=gamma/2;
        x_new = proxg(x-gamma*df(x));
    end
end