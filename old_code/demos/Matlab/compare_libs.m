clear all;close all;
addpath(genpath('../../src_matlab'));
shift_horizon=true;
% noise_amplitude=[0.1;0.1;0.05];
noise_amplitude=[0;0;0];
%%
name = "controller_compare_libs";
[ trailer_controller,initial_state,reference_state,reference_input,obstacle_weights ] = demo_set_obstacles( name,shift_horizon );
%
[state_history,time_history,iteration_history,input_history,simulator] = simulate_demo_trailer(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights,noise_amplitude);
%%
[state_history_forbes,time_history_forbes,iteration_history_forbes] = simulate_demo_trailer_panoc_matlab(trailer_controller,simulator,initial_state,reference_state,reference_input,shift_horizon,noise_amplitude);
%%
[state_history_fmincon,time_history_fmincon_interior_point] = simulate_demo_trailer_fmincon('interior-point',trailer_controller,simulator,initial_state,reference_state,reference_input,shift_horizon,noise_amplitude);
%%
[~,time_history_fmincon_sqp] = simulate_demo_trailer_fmincon('sqp',trailer_controller,simulator,initial_state,reference_state,reference_input,shift_horizon,noise_amplitude);
%%
[~,time_history_fmincon_active_set] = simulate_demo_trailer_fmincon('active-set',trailer_controller,simulator,initial_state,reference_state,reference_input,shift_horizon,noise_amplitude);
%% install OPTI toolbox to use this simulation
[ state_history_ipopt,time_history_ipopt ]  = simulate_demo_trailer_OPTI_ipopt( trailer_controller,simulator, ...
    initial_state,reference_state,reference_input,obstacle_weights,shift_horizon,noise_amplitude);
%%
% [ state_history_,time_history_ ] = simulate_demo_trailer_casadi_ipopt( trailer_controller, ...
%     initial_state,reference_state,reference_input,obstacle_weights,shift_horizon );
%% install draft panoc to use this simulation
[ state_history_draft,time_history_draft,iteration_history_draft ] = simulate_demo_trailer_panoc_draft( trailer_controller, simulator, ...
    initial_state,reference_state,reference_input,shift_horizon,noise_amplitude);
%%
% figure(1);clf;hold all;
nmpccodegen.example_models.trailer_printer(state_history,0.2,'black');
% nmpccodegen.example_models.trailer_printer(state_history_forbes,0.03,'black');
% nmpccodegen.example_models.trailer_printer(state_history_fmincon,0.03,'blue');
nmpccodegen.example_models.trailer_printer(state_history_ipopt,0.2,'green');
% nmpccodegen.example_models.trailer_printer(state_history_draft,0.03,'green');

ylabel('y coordinate');
xlabel('x coordinate');
title('Black = Panoc Green = interior point ipopt');
%%
figure(2);clf;
semilogy(time_history); hold all;
semilogy(time_history_forbes);
semilogy(time_history_fmincon_interior_point);
semilogy(time_history_fmincon_sqp);
semilogy(time_history_fmincon_active_set);
semilogy(time_history_ipopt);
semilogy(time_history_draft)
ylabel('time till convergence (ms)');
xlabel('step');
legend('nmpc-codegen','ForBEs: zeropfr2','fmincon: interior-point','fmincon: sqp','fmincon: active-set','OPTI toolbox: ipopt','panoc draft');
%%
figure(3);clf;
semilogy(time_history,'k.');hold on;
semilogy(time_history_draft,'k--');
semilogy(time_history_forbes,'k:');
semilogy(time_history_ipopt,'kx');
ylabel('time till convergence (ms)');
xlabel('step');
legend(['nmpc-codegen mean time=' num2str(mean(time_history))],...
    ['panoc draft mean time='  num2str(mean(time_history_draft))],...
    ['ForBEs: zeropfr2 mean time=' num2str(mean(time_history_forbes))],...
    ['ipopt mean time='  num2str(mean(time_history_ipopt))]...
    );
%%
figure(4);clf;
hold on;
plot(iteration_history(1:30),'k:');
plot(iteration_history_forbes(1:30),'k--');
ylabel('number of iterations till convergence ');
xlabel('step');
legend('nmpc-codegen','ForBeS zerofpr2');
%%
figure(5);clf;
semilogy(time_history_draft,'k--'); hold all;
semilogy(time_history_fmincon_interior_point,'k:');
semilogy(time_history_fmincon_sqp,'k.');
semilogy(time_history_fmincon_active_set,'kx');
ylabel('time till convergence (ms)');
xlabel('step');
legend(...
    ['panoc draft mean time='  num2str(mean(time_history_draft))],...
    ['fmincon: interior point mean time=' num2str(mean(time_history_fmincon_interior_point))],...
    ['fmincon: sqp mean time='  num2str(mean(time_history_fmincon_sqp))],...
    ['fmincon: active set mean time='  num2str(mean(time_history_fmincon_active_set))]...
    );