clear all;
addpath(genpath('../../src_matlab'));
%%
name="controller_compare_libs"; % change this to demo1,demo2,demo3,demo4 or controller_compare_libs
[ trailer_controller,initial_state,reference_state,reference_input,obstacle_weights ] = demo_set_obstacles( name );

state_history = simulate_demo_trailer(trailer_controller,initial_state,...
    reference_state,reference_input,obstacle_weights);
%% plot states
nmpccodegen.example_models.trailer_printer(state_history,0.03,'red');
%%
fig = gcf;
output_folder = "figures_simulations/";
filename = strcat(output_folder,name,".png");
% filename = [output_folder name '.png'];
saveas(gcf,char(filename));