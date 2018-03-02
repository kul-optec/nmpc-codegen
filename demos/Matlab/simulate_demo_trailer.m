function [ state_history ] = simulate_demo_trailer( trailer_controller, ...
    initial_state,reference_state,reference_input,obstacle_weights )
%SIMULATE_DEMO_TRAILER Simulate 3 seconds of the trailer controller

    % -- simulate controller --
    simulation_time = 3;
    number_of_steps = ceil(simulation_time / trailer_controller.model.step_size);
    % setup a simulator to test
    sim = nmpccodegen.tools.Simulator(trailer_controller.location);
    
    for i=1:length(obstacle_weights)
        sim.set_weight_obstacle(i-1, obstacle_weights(i))
    end

    state = initial_state;
    state_history = zeros(trailer_controller.model.number_of_states, number_of_steps);

    for i=1:number_of_steps
        result_simulation = sim.simulate_nmpc(state, reference_state, reference_input);
        disp(['Step [' num2str(i+1) '/' + num2str(number_of_steps)  ']: The optimal input is: [' ...
              num2str(result_simulation.optimal_input(1)) ',' num2str(result_simulation.optimal_input(2)) ']' ...
              ' time=' result_simulation.time_string ' number of panoc iterations=' ...
              num2str(result_simulation.panoc_interations)]);

        state = trailer_controller.model.get_next_state(state, result_simulation.optimal_input);
        state_history(:, i) = state;
    end
    
    disp("Final state:")
    disp(state)
    
end

