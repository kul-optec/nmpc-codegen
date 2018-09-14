function [ state_history,time_history,iteration_history ] = simulate_panoc_draft( trailer_controller, simulator, ...
    initial_state,reference_state,reference_input,shift_horizon,noise_amplitude )
%SIMULATE_DEMO_TRAILER_PANOC_MATLAB Summary of this function goes here
%   Detailed explanation goes here
    % -- simulate controller --
    simulation_time = 3;
    number_of_steps = ceil(simulation_time / trailer_controller.model.step_size);
    % setup a simulator to test
    
    %% panocdraft specific stuff
    problem.dimension = trailer_controller.model.number_of_inputs*trailer_controller.horizon;
    problem.constraint_type = 'box';
    problem.upper_bound=100;
    problem.lower_bound=0;
    problem.cost_function='cost_func';

    solver_params.tolerance = 1e-3;
    solver_params.buffer_size = 150;
    solver_params.max_iterations = 1000;
    
    panoc('init',problem,solver_params);
    %%
    inputs = repmat(zeros(trailer_controller.model.number_of_inputs, 1), ...
        trailer_controller.horizon, 1);
    
    %%
    state = initial_state;
    state_history = zeros(trailer_controller.model.number_of_states, number_of_steps);
    time_history = zeros(number_of_steps,1);
    iteration_history = zeros(number_of_steps,1);    
    
    for i=1:number_of_steps
        cost = @(inputs_horizon) simulator.evaluate_cost_gradient(...
            state,reference_state,reference_input,inputs_horizon);
        to=tic;
        
        iteration_history(i) = panoc('solve',inputs,cost);
        
        time_history(i)=toc(to)*1000;% get time in ms      
        
        optimal_input=inputs(1:trailer_controller.model.number_of_inputs);
        if(shift_horizon)
            inputs(1:end-trailer_controller.model.number_of_inputs) = ...
                inputs(trailer_controller.model.number_of_inputs+1:end); 
        end
        disp(['panoc draft [' num2str(i) '/' num2str(number_of_steps) ']' ' The optimal input is[' num2str(optimal_input(1)) ' ; ' num2str(optimal_input(2)) '] in ' num2str(iteration_history(i)) ' iterations']);
        
        state = trailer_controller.model.get_next_state_double(state, optimal_input)+((rand - 0.5)*2)*noise_amplitude;
        state_history(:, i) = state;
    end
    
    disp("Final state:")
    disp(state)
    panoc('cleanup');
    
    clear('sim'); % remove the simulator so it unloads the shared lib
end


