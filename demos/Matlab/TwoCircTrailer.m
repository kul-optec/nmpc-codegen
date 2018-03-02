step_size=0.03;

% Q and R matrixes determined by the control engineer.
Q = diag([1. 1. 0.0])*0.2;
R = diag([1. 1.]) * 0.01;

Q_terminal = diag([1. 1. 0.0])*2;
R_terminal = diag([1. 1.]) * 0.01;

trailer_controller = prepare_demo_trailer(step_size,Q,R,Q_terminal,R_terminal);

trailer_controller.horizon = 50; % NMPC parameter
trailer_controller.integrator_casadi = true; % optional  feature that can generate the integrating used  in the cost function
trailer_controller.panoc_max_steps = 500; % the maximum amount of iterations the PANOC algorithm is allowed to do.
trailer_controller.min_residual=-3;

% construct left circle
left_circle = nmpccodegen.controller.obstacles.Obstacle_circular([0.2; 0.2],0.2);

% construct right circle
right_circle = nmpccodegen.controller.obstacles.Obstacle_circular([0.7; 0.2], 0.2);

% add obstacles to controller
trailer_controller = trailer_controller.add_obstacle(left_circle);
trailer_controller = trailer_controller.add_obstacle(right_circle);

% generate the dynamic code
trailer_controller.generate_code();

% simulate everything
initial_state = [0.2; 0.6; 0];
reference_state = [0.7; -0.02; pi/2];
reference_input = [0; 0];

obstacle_weights = [1000.; 1000.];

% state_history = simulate_demo(trailer_controller,initial_state,...
%     reference_state,reference_input,obstacle_weights);