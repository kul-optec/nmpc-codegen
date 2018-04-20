clear all;
addpath(genpath('../../src_matlab'));
shift_horizon=true;
%%
name = "controller_compare_libs";
[ trailer_controller,initial_state,reference_state,reference_input,obstacle_weights ] = demo_set_obstacles( name,shift_horizon );
%%
[state_history,time_history,iteration_history,simulator] = simulate_demo_trailer(trailer_controller,initial_state,reference_state,reference_input,obstacle_weights);
%%
[state_history_forbes,time_history_forbes,iteration_history_forbes] = simulate_demo_trailer_panoc_matlab(trailer_controller,simulator,initial_state,reference_state,reference_input,shift_horizon);
%%
[state_history_fmincon,time_history_fmincon_interior_point] = simulate_demo_trailer_fmincon('interior-point',trailer_controller,simulator,initial_state,reference_state,reference_input,shift_horizon);
%%
[~,time_history_fmincon_sqp] = simulate_demo_trailer_fmincon('sqp',trailer_controller,simulator,initial_state,reference_state,reference_input,shift_horizon);
%%
[~,time_history_fmincon_active_set] = simulate_demo_trailer_fmincon('active-set',trailer_controller,simulator,initial_state,reference_state,reference_input,shift_horizon);
%%
[ state_history_ipopt,time_history_ipopt ]  = simulate_demo_trailer_OPTI_ipopt( trailer_controller,simulator, ...
    initial_state,reference_state,reference_input,obstacle_weights,shift_horizon );
%%
% [ state_history_,time_history_ ] = simulate_demo_trailer_casadi_ipopt( trailer_controller, ...
%     initial_state,reference_state,reference_input,obstacle_weights,shift_horizon );
%%
nmpccodegen.example_models.trailer_printer(state_history,0.03,'red');
nmpccodegen.example_models.trailer_printer(state_history_forbes,0.03,'black');
nmpccodegen.example_models.trailer_printer(state_history_fmincon,0.03,'blue');
% nmpccodegen.example_models.trailer_printer(state_history_ipopt,0.03,'green');

ylabel('y coordinate');
xlabel('x coordinate');
title('black = Forbes red=nmpc-codegen blue=fmincon interior point');
%%
figure;
set(gca, 'YScale', 'log')
hold on;
semilogy(time_history);
semilogy(time_history_forbes);
semilogy(time_history_fmincon_interior_point);
semilogy(time_history_fmincon_sqp);
semilogy(time_history_fmincon_active_set);
semilogy(time_history_ipopt);
ylabel('time till convergence (ms)');
xlabel('step');
legend('nmpc-codegen','ForBEs: zeropfr2','fmincon: interior-point','fmincon: sqp','fmincon: active-set','OPTI toolbox: ipopt');
%%
figure;
hold on;
plot(iteration_history);
plot(iteration_history_forbes);
ylabel('number of iterations till convergence ');
xlabel('step');
legend('nmpc-codegen','ForBEs');