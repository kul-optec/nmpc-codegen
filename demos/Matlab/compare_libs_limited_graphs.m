clear all;close all;
addpath(genpath('../../src_matlab'));
shift_horizon=true;
% noise_amplitude=[0.1;0.1;0.05].*2;
noise_amplitude=[0;0;0];
%%
name = "controller_compare_libs";
[ trailer_controller,initial_state,reference_state,reference_input,obstacle_weights ] = demo_set_obstacles( name,shift_horizon );
%
[state_history,time_history,iteration_history,input_history,simulator] = simulate_demo_trailer(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights,noise_amplitude);
%% install OPTI toolbox to use this simulation
[ state_history_ipopt,time_history_ipopt ]  = simulate_demo_trailer_OPTI_ipopt( trailer_controller,simulator, ...
    initial_state,reference_state,reference_input,obstacle_weights,shift_horizon,noise_amplitude);
%% install draft panoc to use this simulation
[ state_history_draft,time_history_draft,iteration_history_draft ] = simulate_demo_trailer_panoc_draft( trailer_controller, simulator, ...
    initial_state,reference_state,reference_input,shift_horizon,noise_amplitude);
%%
nmpccodegen.example_models.trailer_printer(state_history,0.1,'black');hold all;
nmpccodegen.example_models.trailer_printer(state_history_ipopt,0.1,'green');
plot(initial_state(1),initial_state(2),'kO');
plot(reference_state(1),reference_state(2),'k*');
title('PANOC=black ipopt=green');

ylabel('y coordinate');
xlabel('x coordinate');
%%
% figure;
% set(gca, 'YScale', 'log')
% hold on;
% semilogy(time_history);
% semilogy(time_history_ipopt);
% semilogy(time_history_draft)
% ylabel('time till convergence (ms)');
% xlabel('step');
% legend('nmpc-codegen','ForBEs: zeropfr2','fmincon: interior-point','fmincon: sqp','fmincon: active-set','OPTI toolbox: ipopt','panoc draft');
%%
figure(2);clf;
set(gca, 'YScale', 'log')
hold on;
semilogy(time_history,'k--');
semilogy(time_history_draft,'kx');
semilogy(time_history_ipopt,'k:');
ylabel('time till convergence (ms)');
xlabel('step');
legend(['nmpc-codegen mean time=' num2str(mean(time_history))],...
    ['panoc draft mean time='  num2str(mean(time_history_draft))],...
    ['ipopt mean time='  num2str(mean(time_history_ipopt))]...
    );
%%
% figure;
% hold on;
% plot(iteration_history);
% plot(iteration_history_forbes);
% plot(iteration_history_draft);
% ylabel('number of iterations till convergence ');
% xlabel('step');
% legend('nmpc-codegen','ForBEs','panoc draft');