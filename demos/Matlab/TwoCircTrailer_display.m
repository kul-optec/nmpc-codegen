clear all;
load('TwoCircTrailer.mat');
load('TwoCircTrailer_constraint.mat');
load('TwoCircTrailer_constraint_LA.mat');
%% Display the simulation data
figure(1);clf;
semilogy(iteration_history,'k--');hold all;
semilogy(iteration_history_constraint,'kx');
semilogy(iteration_history_constraint_LA,'k:');
title('amount of iterations till convergence');
xlabel('simulation step');
ylabel('amount of iterations');
legend('no constraint','fixed soft constraint','LA soft constraint');
saveas(gcf,'./figures_simulations/LA_sim_iterations.png')
%%
figure(2);clf;
semilogy(time_history,'k--');hold all;
semilogy(time_history_constraint,'kx');
semilogy(time_history_constraint_LA,'k:');
title('time till convergence');
xlabel('simulation step');
ylabel('time till convergence (ms)');
legend('no constraint','fixed soft constraint','LA soft constraint');
saveas(gcf,'./figures_simulations/LA_sim_time.png')
%% calculate speed
speed=zeros(length(state_history),1);
speed_constraint=zeros(length(state_history),1);
speed_constraint_LA=zeros(length(state_history),1);
for i=1:length(state_history)
    speed(i) = sqrt(sum(input_history(:,i).^2));
    speed_constraint(i) = sqrt(sum(input_history_constraint(:,i).^2));
    speed_constraint_LA(i) = sqrt(sum(input_history_constraint_LA(:,i).^2));
end
figure(3);clf;
plot(speed,'k--');hold on;
plot(speed_constraint,'kx');
plot(speed_constraint_LA,'k:');
legend('no constraint','fixed soft constraint','LA soft constraint');
title('Speed of trailer');
xlabel('simulation step');
ylabel('speed trailer');
saveas(gcf,'./figures_simulations/LA_sim_speed.png');