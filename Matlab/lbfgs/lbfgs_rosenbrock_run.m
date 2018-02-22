clc;
%%
a=1;
b=100;
f =@(x) (a-x(1))^2 + b*(x(2)-x(1))^2;
df = @(x) [-2*(a-(b+1)*x(1)+b*x(2)); 2*b*(x(2)-x(1)) ];
theoretical_solution=[a;a^2];

%%
dimension=2;
number_of_iterations=40; % number of iterations
x0=[-1.2;1.];

buffer_size=20; % buffer_size

% internal buffers used
alpha=zeros(1,buffer_size);
beta=zeros(1,buffer_size);

s=zeros(dimension,buffer_size); % x_{k+1} - x_{k}
y=zeros(dimension,buffer_size); % df(x_{k+1}) - df(x_{k})

% array to save x values that need to be printed on the surface plot
x_steps=zeros(dimension,number_of_iterations);

x=x0;
for interation_index=1:number_of_iterations
    [s_new,y_new,x_new] = lbfgs(interation_index,buffer_size,x,df,s,y);
    x_steps(:,interation_index)=x_new;
    disp(['i=' num2str(interation_index) ' step x1=' num2str(x(1)) ' x2='  num2str(x(2)) ' with cost=' num2str(f(x))]);
    x=x_new;s=s_new;y=y_new;
end

% x_steps = [x0 x_steps];
%% plot the function

% create a grid
x = linspace(-2,2,100);
y = linspace(-2,2,100);
[X,Y] = meshgrid(x,y);
Z=X;

% evaluate the function on the grid
for i=1:size(X,1)
    for j=1:size(X,2)
        Z(i,j)=f([X(i,j);Y(i,j)]);
    end
end

% plot the surface
% figure(1);clf;
% contour(X,Y,Z);

%% plot the convergence

figure(2);clf;
subplot(2,1,1);
plot(abs(x_steps(1,2:end)-theoretical_solution(1))./abs(x_steps(1,1:end-1)-theoretical_solution(1)));
subplot(2,1,2);
plot(abs(x_steps(1,2:end)-theoretical_solution(1))./abs(x_steps(1,1:end-1)-theoretical_solution(1)));
