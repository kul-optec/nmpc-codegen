% f=function
% df=gradient of function
% g_i=df(x(i))

% The buffer of length m contains 2 variables
% s_i = x_{i+1} - x_{i}
% y_i = g_{i+1} - g_{i}

function [ s,y,new_x] = lbfgs(iteration_index,buffer_size,x,df,s,y)
    % if this is the first time, use the gradient descent
    if(iteration_index==1)
        direction=df(x);
        new_x = x-direction;
        % start to fill in the 
        s(:,1) = new_x-x;
        y(:,1) = df(new_x) - df(x);
    else
        % if we dont have enough past values lower the max buffer size
        if(iteration_index<=buffer_size+1)
            buffer_size_max=iteration_index-1;
        else
            buffer_size_max=buffer_size; % maximum buffer size
        end
        
        q=df(x);
        rho=zeros(1,buffer_size_max);
        alpha=zeros(1,buffer_size_max);
        beta=zeros(1,buffer_size_max);
        
        % loop over most recent to oldest
        for i=1:buffer_size_max
            rho(i)=1/(y(:,i)'*s(:,i));
            
            alpha(i) = rho(i)*s(:,i)'*q;
            q = q - alpha(i)*y(:,i);
        end

        z=(y(:,buffer_size_max)*s(:,buffer_size_max)'*q)...
            /(y(:,buffer_size_max)'*y(:,buffer_size_max));
        
        for i=buffer_size_max:-1:1 % oldest first 
            beta(i)=rho(i)*y(:,i)'*z;
            z=z+s(:,i)*(alpha(i) - beta(i));
        end
        
        new_x = x - z; % z is upward direction
        
        % After the new values have been found, 
        % fix the buffers for the next iteration.
        s(:,2:end)=s(:,1:end-1);
        y(:,2:end)=y(:,1:end-1);
        s(:,1) = new_x-x;
        y(:,1) = df(new_x) - df(x);
    end
    
    
end