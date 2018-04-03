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
rectangular_up = nmpccodegen.controller.obstacles.Obstacle_rectangular([1;0.5],0.4,0.5);

% construct lower rectangular
rectangular_down = nmpccodegen.controller.obstacles.Obstacle_rectangular([1; -0.2], 0.4, 0.5);

% construct circle
circle = nmpccodegen.controller.obstacles.Obstacle_circular([0.2;0.2],0.2);

% add obstacles to controller
trailer_controller = trailer_controller.add_obstacle(rectangular_up);
trailer_controller = trailer_controller.add_obstacle(rectangular_down);
trailer_controller = trailer_controller.add_obstacle(circle);

% generate the dynamic code
trailer_controller.generate_code();
%%
% simulate everything
initial_state = [-0.1; -0.1; pi];
reference_state = [1.5; 0.4; 0];
reference_input = [0; 0];

obstacle_weights = [10.;10.;2000.];

state_history = simulate_demo_trailer(trailer_controller,initial_state,...
    reference_state,reference_input,obstacle_weights);
%% 
figure;
hold all;
rectangular_up.plot();
rectangular_down.plot();
circle.plot();
nmpccodegen.example_models.trailer_printer(state_history,0.03,'red');