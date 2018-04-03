clear all;
addpath(genpath('../../src_matlab'));
%%
step_size=0.03;

% Q and R matrixes determined by the control engineer.
Q = diag([1. 1. 0.01])*0.2;
R = diag([1. 1.]) * 0.01;

Q_terminal = Q;
R_terminal = R;

controller_folder_name = 'demo_controller_matlab';
trailer_controller = prepare_demo_trailer(controller_folder_name,step_size,Q,R,Q_terminal,R_terminal);
%%
trailer_controller.horizon = 50; % NMPC parameter
trailer_controller.integrator_casadi = true; % optional  feature that can generate the integrating used  in the cost function
trailer_controller.panoc_max_steps = 500; % the maximum amount of iterations the PANOC algorithm is allowed to do.
trailer_controller.min_residual=-3;
trailer_controller.lbgfs_buffer_size = 50;

% construct upper rectangular
costum_obstacle = nmpccodegen.controller.obstacles.Obstacle_nonconvex_constraints();
h_0 = @(x) x(1)-x(0)^2;
h_1 = @(x) 1 + (x(0)^2)/2 - x(1);
costum_obstacle = costum_obstacle.add_constraint(h_0);
costum_obstacle = costum_obstacle.add_constraint(h_1);

% add obstacles to controller
trailer_controller = trailer_controller.add_obstacle(costum_obstacle);

% generate the dynamic code
trailer_controller.generate_code();
%%
% simulate everything
initial_state = [-1.0; 0.0; pi/2];
reference_state = [-1.0; 2.; pi/3];
reference_input = [0; 0];

obstacle_weights = 1e3;

state_history = simulate_demo_trailer(trailer_controller,initial_state,...
    reference_state,reference_input,obstacle_weights);
%% 
figure;
hold all;
nmpccodegen.example_models.trailer_printer(state_history,0.03,'red');
h_0_border = @(x) x.^2;
h_1_border = @(x) 1 + (x.^2)/2;
draw_obstacle_border(h_0_border,[-2;2],100);
draw_obstacle_border(h_1_border, [-2;2], 100);
