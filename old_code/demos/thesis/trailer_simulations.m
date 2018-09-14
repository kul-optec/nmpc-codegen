% closed-loop simulation

close all
clear
cmap = colormap('lines');
set(0,'DefaultAxesFontSize',12)
%% system parameters

L           = 0.5;  % length of the trailer
axle_length = 0.4;

params_sys = {L};

%% number of states, inputs, outputs
n_states = 3;
n_in = 2;
n_out = 3;

%% simulation parameters

ts = 0.05;               % sampling time
T_sim = 10;              % simulation time
T_hor = 1.5;             % horizon time

N_sim = ceil(T_sim/ts);  % simulation steps
N_hor = ceil(T_hor/ts);  % horizon length

%% optimal control problem parameters

epsilon = 5e-3;         % tolerance
bet = 0.2;              % penalty on the state
del = 0.01;             % penalty on the input
mu  = 700;              % penalty on the state constraint violation
x_ref = [7; 5; 0.8];    % target point
obstacle(1).xc = [1.5; 0]; % obstacle: center
obstacle(1).r  = 1;        % obstable: radius
obstacle(2).xc = [3.5; 2]; % obstacle: center
obstacle(2).r  = 0.6;      % obstable: radius
obstacle(3).xc = [2;2.5];  % obstacle: center
obstacle(3).r  = 0.8;      % obstable: radius
obstacle(4).xc = [5;4];  % obstacle: center
obstacle(4).r  = 1.05;      % obstable: radius
Qterm = 0.8;            % penalty parameter of terminal cost
params_noc = {bet, del, mu, x_ref, obstacle};

%% select integrator

integrator = @integrator_runge_kutta_4;

%% Entering the starting position of the trailer

x_rest = [0; -0.5; pi/2];

%% bounds

u_min = -10;
u_max = +10;

us_min = repmat(u_min*ones(n_in,1), N_hor, 1);
us_max = repmat(u_max*ones(n_in,1), N_hor, 1);

%% define single-shooting formulation

us = casadi.SX.sym('us', n_in*N_hor);
x0 = casadi.SX.sym('x0', n_states);
Q = 0;
x_curr = x0;

for k = 1:N_hor
    u_curr = us((k-1)*n_in+1:k*n_in);
    [x_curr, Q] = integrator(@trailer_kinematics, x_curr, Q, u_curr, ts, params_sys{:}, params_noc{:});
end
Q = Q + Qterm * norm(x_curr - x_ref)^2;


%% compile functions
costfun_u = casadi.Function('trailer', {us, x0}, {Q, jacobian(Q, us)'});
mexify(costfun_u, 'trailer');
costfun_u.generate('trailer2');

%% simulate system using zerofpr2 to solve problem

names{1} = 'ZeroFPR2';
fprintf('%s...\n', names{end});
opt_zerofpr2.tol = epsilon;
opt_zerofpr2.display = 0;
opt_zerofpr2.maxit = 10000;
opt_zerofpr2.adaptive = 1;
opt_zerofpr2.solver = 'zerofpr2';
opt_zerofpr2.method = 'lbfgs';
opt_zerofpr2.linesearch = 'backtracking';
opt_zerofpr2.report = 1;
g = indBox(u_min, u_max);
ts_zerofpr2 = zeros(1, N_sim);
x_curr = x_rest;
x_all_zerofpr2 = x_rest;
us0 = repmat(zeros(n_in, 1), N_hor, 1);
%us0 =  [-7.9148; 9.1265; -6.5024; 0.1835]; %To remove
no_iter_fpr2 = [];
U = [];
U_optisol = [];
for k = 1:N_sim
    cost_forbes = @(myus) wrap_f_gradf(@trailer_mex, 'trailer', myus, x_curr);
    % embed cost function in an object that ForBES can use
    f = smoothFunction(cost_forbes);
    % solve problem
    t0 = tic;
    out_zerofpr2 = forbes(f, g, us0, [], [], opt_zerofpr2);
    ts_zerofpr2(k) = toc(t0);
    % extract the control from first sampling period
    u_curr = out_zerofpr2.x(1:n_in);
    U_optisol = [U_optisol, out_zerofpr2.x];
    U = [U, u_curr];
    % asser that norm(out_zerofpr2.solver.residual) smaller than tol =
    % 10^-3
    % set initial iterate for next problem
    us0 = [out_zerofpr2.x(n_in+1:end); zeros(n_in, 1)];
    % simulate nonliner dynamics during a sampling interval using the computed input
    [~, x_ode45] = ode45(@(t, x) trailer_kinematics(x, u_curr, params_sys{:}), [0, ts], x_curr);
    x_curr = x_ode45(end,:)';% + rands(3,1)*0.00.*abs(x_ode45(end,:)' - x_all_zerofpr2(k));
    x_all_zerofpr2 = [x_all_zerofpr2, x_curr];
    no_iter_fpr2 = [no_iter_fpr2, out_zerofpr2.solver.iterations];
end






%% simulate system using ipopt-ss to solve problem

names{end+1} = 'IPOPT-SS';
fprintf('%s...\n', names{end});
nlp = struct('x', us, 'p', x0, 'f', Q);
opts_nlpsol = struct();
opts_nlpsol.print_time = false;
opts_nlpsol.ipopt.print_level = 0;
opts_nlpsol.ipopt.tol = epsilon;
S = casadi.nlpsol('S', 'ipopt', nlp, opts_nlpsol);
ts_ipopt_ss = zeros(1, N_sim);
x_curr = x_rest;
us0 = repmat(zeros(n_in, 1), N_hor, 1);
U_ipopt = [];
X_ipopt = [x_rest];
for k = 1:N_sim
    t0 = tic();
    sol_ipopt_ss = S('lbx',us_min,'ubx',us_max,'p',x_curr,'x0',us0);
    ts_ipopt_ss(k) = toc(t0);
    us_curr = full(sol_ipopt_ss.x);
    %     f_curr = full(sol_ipopt_ss.f);
    u_curr = us_curr(1:n_in);
    U_ipopt = [U_ipopt, u_curr];
    us0 = [us_curr(n_in+1:end); zeros(n_in, 1)];
    [~, x_ode45] = ode45(@(t, x) trailer_kinematics(x, u_curr, params_sys{:}), [0, ts], x_curr);
    x_curr = x_ode45(end,:)' + rands(3,1)*0.00.*abs(x_ode45(end,:)' - X_ipopt(k));
    X_ipopt = [X_ipopt, x_curr];
end

fprintf('Solver time using ZeroFPR2 = %f...\n Solver time using IPOPT = %f \n',sum(ts_zerofpr2), sum(ts_ipopt_ss));


%% Plot trajectory of the centre of mass
figure(1), hold on
plot(x_all_zerofpr2(1,:), x_all_zerofpr2(2,:), 'Color', cmap(1,:), 'linewidth', 2)
plot(X_ipopt(1,:), X_ipopt(2,:), '--', 'Color', [0.8 0.8 0.8],'linewidth', 2)
angles = 0:0.01:2*pi;
for j=1:length(obstacle)
    obs = obstacle(j);
    plot(obs.r * cos(angles) + obs.xc(1), obstacle(j).r * sin(angles)+ obstacle(j).xc(2), ...
        'Color', cmap(5,:), 'linewidth', 3);
    plot(obs.xc(1), obs.xc(2), '+', 'Color', cmap(5,:), 'linewidth', 2, 'markersize', 7)
end
plot(x_ref(1), x_ref(2), 'x', 'Color', cmap(7,:), 'linewidth', 2, 'markersize', 8);
grid on
xlabel('x');
ylabel('y');
axis equal
hold off


%% Plot both wheels
figure(3),  hold on;
[x_left_fpr2, x_right_fpr2] = trailer_axle_plot(x_all_zerofpr2, L, axle_length);
plot(x_left_fpr2(1,:), x_left_fpr2(2,:),'linewidth', 2,'Color', cmap(2,:))
plot(x_right_fpr2(1,:), x_right_fpr2(2,:),'linewidth', 2,'Color', cmap(1,:))
plot(x_ref(1), x_ref(2), 'x', 'linewidth', 3);
for j=1:length(obstacle)
    obs = obstacle(j);
    effective_radius = obs.r - axle_length;
    rectangle('Position',[obs.xc-effective_radius; 2*effective_radius;2*effective_radius], ...
    'curvature', [1 1], 'Facecolor', cmap(3,:))
    plot(obs.xc(1), obs.xc(2), '+', 'Color', cmap(5,:), 'linewidth', 2, 'markersize', 7)
end
axis equal
grid on
xlabel('x');
ylabel('y');
legend('left wheel', 'right wheel', 'location','southeast')

%{
%% Plot control actions
figure(4)
plot((1:N_sim)*ts , U', 'linewidth', 2)
axis tight
grid on;
xlabel('Time (s)')
ylabel('Control action');

%% Plot states vs time
figure(5)
plot((0:N_sim)*ts, x_all_zerofpr2', 'linewidth', 2)
axis tight
grid on;
xlabel('Time (s)')
ylabel('States');
legend('x','y','heading')

%% Compute second-order partial gradients
n = n_in*N_hor;
JQ = jacobian(Q, us)';
preconditioner = [];
for i=1:n
    preconditioner = [preconditioner; 1/sqrt(jacobian(JQ(i), us(i)))];
end
preconditionerFunction = casadi.Function('Dprecond', {us, x0}, {preconditioner});


%% Times
figure(7); hold on;
plot((2:N_sim)*ts,ts_zerofpr2(2:end), 'linewidth', 2); 
plot((2:N_sim)*ts,ts_ipopt_ss(2:end), 'linewidth', 2);
grid on;
xlabel('Time (s)')
ylabel('Runtime');
legend('PANOC', 'IPOPT');
%}