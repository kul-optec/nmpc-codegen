clear all;
addpath(genpath('../../src_matlab'));
%%
step_size=0.05;

% Q and R matrixes determined by the control engineer.
Q = diag([1. 1. 1.])*0.2;
R = diag([1. 1.]) * 0.01;

Q_terminal = diag([1. 1. 1])*10;
R_terminal = diag([1. 1.]) * 0.01;

noise_amplitude=[0;0;0];

controller_folder_name = 'demo_controller_matlab';
trailer_controller = prepare_demo_trailer(controller_folder_name,step_size,Q,R,Q_terminal,R_terminal);

trailer_controller.horizon = 40; % NMPC parameter
trailer_controller.integrator_casadi = true; % optional  feature that can generate the integrating used  in the cost function
trailer_controller.panoc_max_steps = 1000000; % the maximum amount of iterations the PANOC algorithm is allowed to do.
trailer_controller.min_residual=-3;
trailer_controller.lbgfs_buffer_size=7;
% trailer_controller.pure_prox_gradient=true;
trailer_controller.shift_input=true;

% construct left circle
circle1 = nmpccodegen.controller.obstacles.Circular([1.5; 0.], 1., trailer_controller.model);
circle2 = nmpccodegen.controller.obstacles.Circular([3.5; 2.], 0.6, trailer_controller.model);
circle3 = nmpccodegen.controller.obstacles.Circular([2.; 2.5], 0.8, trailer_controller.model);
circle4 = nmpccodegen.controller.obstacles.Circular([5.; 4.], 1.05, trailer_controller.model);

% add obstacles to controller
trailer_controller = trailer_controller.add_constraint(circle1);
trailer_controller = trailer_controller.add_constraint(circle2);
trailer_controller = trailer_controller.add_constraint(circle3);
trailer_controller = trailer_controller.add_constraint(circle4);

% generate the dynamic code
trailer_controller.generate_code();

% simulate everything
initial_state = [0.; -0.5 ; pi/2];
reference_state = [7.; 5.; 0.8];
reference_input = [0; 0];

obstacle_weights = [700.;700.;700.;700.];
%%
[state_history,time_history,iteration_history,input_history,simulator] = simulate_demo_trailer(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights,noise_amplitude);
simulator.force_unload();
clear simulator;
%%
trailer_controller.lbgfs_buffer_size=2;
trailer_controller.generate_code();
[state_history_small_buffer,time_history_small_buffer,iteration_history_small_buffer,~,~] = simulate_demo_trailer(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights,noise_amplitude);
%% 
trailer_controller.lbgfs_buffer_size=200;
trailer_controller.generate_code();
[state_history_big_buffer,time_history_big_buffer,iteration_history_big_buffer,~,~] = simulate_demo_trailer(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights,noise_amplitude);
%%
trailer_controller.pure_prox_gradient = true;
trailer_controller.generate_code();
[state_history_pure_prox,time_history_pure_prox,iteration_history_pure_prox,~,~] = simulate_demo_trailer(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights,noise_amplitude);
%%
figure;
hold on;
nmpccodegen.example_models.trailer_printer(state_history,0.03,'red');
nmpccodegen.example_models.trailer_printer(state_history_pure_prox,0.03,'black');
circle1.plot();
circle2.plot();
circle3.plot();
circle4.plot();
ylabel('y coordinate');
xlabel('x coordinate');
title('black =no lbfgs red=with bfgs');
%%
figure;
show_steps = 1:30;
set(gca, 'YScale', 'log')
hold on;
semilogy(time_history(show_steps),'k.');
semilogy(time_history_small_buffer(show_steps),'k--');
semilogy(time_history_big_buffer(show_steps),'k:');
semilogy(time_history_pure_prox(show_steps),'kx');
ylabel('time till convergence (ms)');
xlabel('step');
legend('with L-BFGS buffersize=7','with L-BFGS buffersize=2','with L-BFGS buffersize=200','no L-BFGS');
%%
figure;
show_steps = 1:30;
set(gca, 'YScale', 'log')
hold on;
semilogy(iteration_history(show_steps),'k.');
semilogy(iteration_history_small_buffer(show_steps),'k--');
semilogy(iteration_history_big_buffer(show_steps),'k:');
semilogy(iteration_history_pure_prox(show_steps),'kx');
ylabel('number of iterations till convergence');
xlabel('step');
legend('with L-BFGS buffersize=7','with L-BFGS buffersize=2','with L-BFGS buffersize=200','no L-BFGS');