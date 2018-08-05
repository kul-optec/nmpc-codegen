function [ state_history,time_history,iteration_history,sim ] = simulate_demo_controller( controller, ...
    initial_state,reference_state,reference_input,obstacle_weights,noise_amplitude )
%SIMULATE_DEMO_CONTROLLER Simulate 3 seconds of the quadcopter controller

    % -- simulate controller --
    simulation_time = 3;
    number_of_steps = ceil(simulation_time / controller.model.step_size);
    % setup a simulator to test
    sim = nmpccodegen.tools.Simulator(controller.location);
    
    for i=1:length(obstacle_weights)
        sim.set_weight_constraint(i-1, obstacle_weights(i))
    end

    state = initial_state;
    state_history = zeros(controller.model.number_of_states, number_of_steps);
    time_history = zeros(number_of_steps,1);
    iteration_history = zeros(number_of_steps,1);
    
    for i=1:number_of_steps
        result_simulation = sim.simulate_nmpc(state, reference_state, reference_input);
        disp(['Step [' num2str(i) '/'  num2str(number_of_steps)  ']: The optimal input is: [' ...
              num2str(result_simulation.optimal_input(1)) ',' num2str(result_simulation.optimal_input(2)) ...
               ',' num2str(result_simulation.optimal_input(3))  ',' num2str(result_simulation.optimal_input(4)) ']' ...
              ' time=' result_simulation.time_string ' number of panoc iterations=' ...
              num2str(result_simulation.panoc_interations)]);

        time_history(i)=result_simulation.seconds*1000+result_simulation.milli_seconds;
        iteration_history(i)=result_simulation.panoc_interations;
        
        state = controller.model.get_next_state_double(state, result_simulation.optimal_input)+((rand - 0.5)*2)*noise_amplitude;
        state_history(:, i) = state;
    end
    
    disp('Final state:');
    disp(state);
    
end

