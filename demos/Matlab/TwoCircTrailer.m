clear all;
addpath(genpath('../../src_matlab'));
shift_horizon=false;
noise_amplitude=[0;0;0];
%%
step_size=0.03;

% Q and R matrixes determined by the control engineer.
Q = diag([1. 1. 0.0])*0.2;
R = diag([1. 1.]) * 0.01;

Q_terminal = diag([1. 1. 0.01])*2;
R_terminal = diag([1. 1.]) * 0.01;

controller_folder_name = 'demo_controller_matlab';
trailer_controller = prepare_demo_trailer(controller_folder_name,step_size,Q,R,Q_terminal,R_terminal);

trailer_controller.horizon = 50; % NMPC parameter
trailer_controller.integrator_casadi = true; % optional  feature that can generate the integrating used  in the cost function
trailer_controller.panoc_max_steps = 500; % the maximum amount of iterations the PANOC algorithm is allowed to do.
trailer_controller.min_residual=-3;

% construct left circle
left_circle = nmpccodegen.controller.obstacles.Circular([0.2; 0.2],0.2,trailer_controller.model);

% construct right circle
right_circle = nmpccodegen.controller.obstacles.Circular([0.7; 0.2], 0.2,trailer_controller.model);

% add obstacles to controller
trailer_controller = trailer_controller.add_constraint(left_circle);
trailer_controller = trailer_controller.add_constraint(right_circle);

% experimental feature !!!!
trailer_controller.shooting_mode='single shot';
trailer_Controller.shift_input=shift_horizon;

% generate the dynamic code
trailer_controller.generate_code();
%%
% simulate everything
initial_state = [0.2; 0.6; 0];
reference_state = [0.7; -0.02; pi/2];
reference_input = [0; 0];

obstacle_weights = [1000.; 1000.];

[ state_history,time_history,iteration_history,input_history,~ ] = simulate_demo_trailer(trailer_controller,initial_state,...
    reference_state,reference_input,obstacle_weights,noise_amplitude);
%% plot everything TODO make proper plot !
figure(1);clf
left_circle.plot();
hold on;
right_circle.plot();
nmpccodegen.example_models.trailer_printer(state_history,0.03,'black');
plot(initial_state(1),initial_state(2),'kO')
plot(reference_state(1),reference_state(2),'k*')
title('path trailer');
xlabel('X coordinate');
ylabel('Y coordinate');

figure(2);clf
plot(iteration_history);
title('amount of iterations till convergence');
xlabel('index simulation step');
ylabel('amount of iterations');

%% Save the data
save('TwoCircTrailer.mat','state_history','time_history','iteration_history','input_history');