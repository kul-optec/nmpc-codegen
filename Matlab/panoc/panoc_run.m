% PANOC algorithm using the lbgfs and proximal gradient methods
% include the Matlab folder with all its subfolders to your path
number_of_steps=10;
dimension=2;
x_steps=zeros(dimension,number_of_steps);
taus=zeros(1,number_of_steps);
x0=[0.5;0.5];
% x0=100;
%% variables proximal gradient descent
beta_safety_value=0.05; % safety constant

w=2; 
g = @(x) g_1(x,w);
proxg = @(x) prox_g_1( x,w );
% g = @(x) g_2(x);
% proxg = @(x) prox_g_2( x );

degree_polynomial=20;
f = @(x) sum(x.^degree_polynomial);
df = @(x) (degree_polynomial)*x.^(degree_polynomial-1);

% get starting value gamma
lipschitz_constant= estimate_lipschitz( df,x0 );
gamma0 = (1-beta_safety_value)/lipschitz_constant;
gamma=gamma0;
%% variables lbgfs
buffer_size=50; % buffer_size

% internal buffers used
alpha=zeros(1,buffer_size);
beta=zeros(1,buffer_size);

s=zeros(dimension,buffer_size); % x_{k+1} - x_{k}
y=zeros(dimension,buffer_size); % df(x_{k+1}) - df(x_{k})
%% iterate
x=x0;% set the starting point, and iterate
for interation_index=1:number_of_steps
    [x_prox_grad_descent,new_gamma] = prox_grad_descent_step( x,gamma,beta,proxg,f,df );
    gamma=new_gamma;
    step_prox = (x-x_prox_grad_descent);
    
    R= @(x) (1/gamma)*(x - proxg(x-df(x)*gamma));
    [s_new,y_new,x_lbfgs] = lbfgs(interation_index,buffer_size,x,R,s,y);
    s=s_new;y=y_new;
    
    % find the right convex combination trough backtracking
    tau=1;
    max_number_of_steps_backtracking=100;
    for i=1:max_number_of_steps_backtracking
        d=x_lbfgs-x;
        potential_x=x-(1-tau)*step_prox + tau*d;
        sigma=beta_safety_value/(4*gamma);
        if(FBE( potential_x,gamma,beta_safety_value,f,df,g,proxg  )<= FBE( x,gamma,beta_safety_value,f,df,g,proxg  )-sigma*norm(step_prox/gamma,2)^2)
            break; % if this is statified stop right away
        else
            tau=tau/2;
        end
    end
    x_steps(:,interation_index)=potential_x;
    taus(interation_index)=tau;
end
%% plot the convergence rate
figure(1);clf;
plot(taus);

figure(2);clf;
plot(x_steps(1,2:end)./x_steps(1,1:end-1));