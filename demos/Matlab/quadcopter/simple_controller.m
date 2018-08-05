clear all;
% close all;
noise_amplitude=zeros(12,1);
% noise_amplitude=[ones(6,1)*0.01;zeros(6,1)];
%%
step_size=0.01;

% Q and R matrixes determined by the control engineer.
Q = diag([1e2 1e2 1e2 0. 0. 0. 0. 0. 0. 0. 0. 0. ]);
R = diag([1. 1. 1. 1.])*0.05 ;

Q_terminal = diag([1e2 1e2 1e2 1. 1. 1. 1. 1. 1. 1. 1. 1. ])*2;
R_terminal = R*10;

controller_folder_name = 'quadcopter_matlab';
controller = prepare_demo_quadcopter(controller_folder_name,step_size,Q,R,Q_terminal,R_terminal);

controller.horizon = 100; % NMPC parameter
% controller.integrator_casadi = true; % optional  feature that can generate the integrating used  in the cost function
controller.panoc_max_steps = 10000; % the maximum amount of iterations the PANOC algorithm is allowed to do.
controller.min_residual=-3;
controller.lbgfs_buffer_size=100;

%% Add obstacles
radius =1;
center_coordinates1=[6;0;1.5];
circle1 = nmpccodegen.controller.obstacles.Circular(center_coordinates1,radius,controller.model);

controller = controller.add_constraint(circle1);

center_coordinates2=[9;0;4.5];
circle2 = nmpccodegen.controller.obstacles.Circular(center_coordinates2,radius,controller.model);

controller = controller.add_constraint(circle2);

obstacle_weights=[1e2;1e2]; % weights used for constraints in simulation
%% Generate the C code
controller = controller.generate_code();
%%
initial_state = zeros(12,1);initial_state(3)=2;
reference_state = zeros(12,1);
reference_state(1)=15.;
reference_state(2)=0.;
reference_state(3)=5.;

reference_input=[41;41;41;41]; % hover

%%
[state_history,time_history,iteration_history,simulator] = simulate_demo_controller(controller,initial_state,reference_state,reference_input,obstacle_weights,noise_amplitude);

nmpccodegen.tools.Simulator.force_unload()
%% Visualize the result
% static_casadi_parameters = vertcat(initial_state, reference_state,reference_input);
figure(1);clf;
plot3(state_history(1,:),state_history(2,:),state_history(3,:),'r');
hold all;
plot3(initial_state(1),initial_state(2),initial_state(3),'k*');
plot3(reference_state(1),reference_state(2),reference_state(3),'ko');
disp('--------------------------');
disp(['Quadcopter arrived at point [' num2str(state_history(1,end)) ',' num2str(state_history(2,end)) ',' num2str(state_history(3,end)) ']' ])
disp(['Distance from reference point [' num2str(reference_state(1)) ',' ...
    num2str(reference_state(2)) ',' num2str(reference_state(3)) ']' ...
    '  ' num2str(norm(state_history(1:3,end)-reference_state(1:3)))]);

circle1.plot3();
circle2.plot3();

figure(2);clf; % plot x vs y
circle(center_coordinates1(1),center_coordinates1(2),radius);
circle(center_coordinates2(1),center_coordinates2(2),radius);
hold on;
plot(state_history(1,:),state_history(2,:));
hold off;
xlabel('x');
ylabel('y');

figure(3);clf; % plot x vs z
circle(center_coordinates1(1),center_coordinates1(3),radius);
circle(center_coordinates2(1),center_coordinates2(3),radius);
hold on;
plot(state_history(1,:),state_history(3,:));
hold off;
xlabel('x');
ylabel('z');