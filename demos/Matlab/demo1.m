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
trailer_controller.horizon = 30; % NMPC parameter
trailer_controller.integrator_casadi = true; % optional  feature that can generate the integrating used  in the cost function
trailer_controller.panoc_max_steps = 500; % the maximum amount of iterations the PANOC algorithm is allowed to do.
trailer_controller.min_residual=-3;

rectangular_center_coordinates = [0.45;-0.1];
rectangular_width = 0.4;
rectangular_height = 0.1;
rectangular = nmpccodegen.controller.obstacles.Obstacle_rectangular(rectangular_center_coordinates,...
                                                 rectangular_width,rectangular_height);

% construct left circle
left_circle = nmpccodegen.controller.obstacles.Obstacle_circular([0.2; 0.2],0.2);

% construct right circle
right_circle = nmpccodegen.controller.obstacles.Obstacle_circular([0.7; 0.2], 0.2);

% add obstacles to controller
trailer_controller = trailer_controller.add_obstacle(rectangular);
trailer_controller = trailer_controller.add_obstacle(left_circle);
trailer_controller = trailer_controller.add_obstacle(right_circle);

% generate the dynamic code
trailer_controller.generate_code();
%%
% simulate everything
initial_state = [0.45; 0.1; -pi/2];
reference_state = [0.8; -0.1; 0];
reference_input = [0; 0];

obstacle_weights = [10000.;8000.;50.];

state_history = simulate_demo_trailer(trailer_controller,initial_state,...
    reference_state,reference_input,obstacle_weights);
%% plot everything TODO make proper plot !
figure;
hold all;
rectangular.plot();
left_circle.plot();
right_circle.plot();
nmpccodegen.example_models.trailer_printer(state_history,0.03,'red');