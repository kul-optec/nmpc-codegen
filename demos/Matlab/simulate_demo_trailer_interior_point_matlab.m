function [ state_history,time_history,iteration_history ] = simulate_demo_trailer_interior_point_matlab( trailer_controller, simulator, ...
    initial_state,reference_state,reference_input,shift_horizon )
%SIMULATE_DEMO_TRAILER_PANOC_MATLAB Summary of this function goes here
%   Detailed explanation goes here
    % -- simulate controller --
    simulation_time = 3;
    number_of_steps = ceil(simulation_time / trailer_controller.model.step_size);
    % setup a simulator to test
    
    %% fmincon panoc specific stuff
    A=eye(trailer_controller.model.number_of_inputs*trailer_controller.horizon);
    A = vertcat(A,A);
    b = ones(trailer_controller.model.number_of_inputs*trailer_controller.horizon,1);
    b = vertcat(b*4,b*4);
    
    inputs = repmat(zeros(trailer_controller.model.number_of_inputs, 1), ...
        trailer_controller.horizon, 1);
    
    %%
    state = initial_state;
    state_history = zeros(trailer_controller.model.number_of_states, number_of_steps);
    time_history = zeros(number_of_steps,1);
    iteration_history = zeros(number_of_steps,1);    
    
    for i=1:number_of_steps
        cost = @(inputs_horizon) simulator.evaluate_cost(...
            state,reference_state,reference_input,inputs_horizon);
        to=tic;
        options = optimset('TolFun', 1e-3, 'MaxIter',10000,'MaxFunEvals',10000);
        inputs = fmincon(cost,inputs,A,b,[],[],[],[],[],options);
        time_history(i)=toc(to)*1000;% get time in ms
        iteration_history(i)=0;        
        
        optimal_input=inputs(1:trailer_controller.model.number_of_inputs);
        if(shift_horizon)
            % shift the iputs in prepartion of the next iteration
            inputs(1:end-trailer_controller.model.number_of_inputs) = ...
                inputs(trailer_controller.model.number_of_inputs+1:end); 
        end
        disp(['The optimal input is[' num2str(optimal_input(1)) ' ; ' num2str(optimal_input(2)) ']']);
        
        state = trailer_controller.model.get_next_state_double(state, optimal_input)+((rand - 0.5)*2)*noise_amplitude;
        state_history(:, i) = state;
    end
    
    disp("Final state:")
    disp(state)
    
    clear('sim'); % remove the simulator so it unloads the shared lib
end

