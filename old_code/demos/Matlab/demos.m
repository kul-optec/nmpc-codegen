clear all;
addpath(genpath('../../src_matlab'));
shift_horizon=true;
noise_amplitude=[0;0;0];
%%
name="demo4"; % change this to demo1,demo2,demo3,demo4 or controller_compare_libs
[ trailer_controller,initial_state,reference_state,reference_input,obstacle_weights ] = demo_set_obstacles( name,shift_horizon );

state_history = simulate_demo_trailer(trailer_controller,initial_state,...
    reference_state,reference_input,obstacle_weights,noise_amplitude);
%% plot states
nmpccodegen.example_models.trailer_printer(state_history,0.1,'red');
plot(initial_state(1),initial_state(2),'ko')
plot(reference_state(1),reference_state(2),'k*')
%%
fig = gcf;
output_folder = "figures_simulations/";
filename = strcat(output_folder,name,".png");
% filename = [output_folder name '.png'];
saveas(gcf,char(filename));