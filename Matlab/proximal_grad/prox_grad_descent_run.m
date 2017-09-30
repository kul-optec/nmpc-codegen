% demonstration of the proximal gradient descent
clc;clear all;
number_of_steps=5;
dimension=2;

x0=[0.5;0.5]; % starting position
beta=0.05; % safety constant

w=5; 
g = @(x) g_1(x,w);
proxg = @(x) prox_g_1( x,w );

degree_polynomial=5;
f = @(x) sum(x.^degree_polynomial);
df = @(x) (degree_polynomial)*x.^(degree_polynomial-1);

% get starting value gamma
lipschitz_constant= estimate_lipschitz( df,x0 );
gamma0 = (1-beta)/lipschitz_constant;

%%
x_steps=zeros(dimension,number_of_steps);
x=x0;
gamma=gamma0;
for i=1:number_of_steps
     [new_x,new_gamma] = prox_grad_descent_step( x,gamma,beta,proxg,f,df );
     x=new_x;
     gamma=new_gamma;
     
     x_steps(:,i)=x; % log steps
end
% calculate the convergence
rate_of_convergence= x_steps(:,2:end)./(x_steps(:,1:end-1));
%% Rate of convergence
figure(1);clf;
title('rate of convergence');
semilogy(rate_of_convergence(1,:));
xlabel('step index');ylabel('rate of convergence')
disp(['the average are of convergence is ' num2str(mean(rate_of_convergence(1,:)))])