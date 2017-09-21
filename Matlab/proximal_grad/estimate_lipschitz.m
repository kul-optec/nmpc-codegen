function [ estimation_lipschitz_constant ] = estimate_lipschitz( df,x )
    delta=10^-5;
    estimation_lipschitz_constant = norm((df(x+delta)-df(x))/delta);
end

