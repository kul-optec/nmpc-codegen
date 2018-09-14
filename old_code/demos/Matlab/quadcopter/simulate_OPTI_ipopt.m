function [ state_history,time_history,iteration_history ] = simulate_OPTI_ipopt( controller, simulator, ...
    initial_state,reference_state,reference_input,obstacle_weights,shift_horizon,noise_amplitude)
%SIMULATE_DEMO_TRAILER_PANOC_MATLAB Summary of this function goes here
%   Detailed explanation goes here
    % -- simulate controller --
    simulation_time = 3;
    number_of_steps = ceil(simulation_time / controller.model.step_size);
    % setup a simulator to test
    
    inputs = repmat(zeros(controller.model.number_of_inputs, 1), ...
        controller.horizon, 1);
    
    %%
    state = initial_state;
    state_history = zeros(controller.model.number_of_states, number_of_steps);
    time_history = zeros(number_of_steps,1);
    iteration_history = zeros(number_of_steps,1);    
    
    for i=1:number_of_steps
        cost_f = @(x) simulator.evaluate_cost(...
            state,reference_state,reference_input,x);
        gradient_f = @(x) gradient_f_multiarg(...
            simulator,state,reference_state,reference_input,x);
        
        % Bounds
        lb = ones(controller.horizon*controller.model.number_of_inputs,1).*0;
        ub = ones(controller.horizon*controller.model.number_of_inputs,1).*100;
        
        opts = optiset('solver','ipopt','tolrfun',1e-3,'tolafun',1e-3);
%         Opt = opti('fun',cost_f,'grad',gradient_f,'bounds', lb, ub,'options' ,opts);
        Opt = opti('fun',cost_f,'grad',gradient_f ,'bounds', lb, ub,'options' ,opts);
        to=tic;

        [x,fval,exitflag,info] = solve(Opt,inputs);
        
        
        time_history(i)=toc(to)*1000;% get time in ms
        
        inputs = x;
        iteration_history(i)=0;        
        
        optimal_input=inputs(1:controller.model.number_of_inputs);
        if(shift_horizon)
            inputs(1:end-controller.model.number_of_inputs) = ...
                inputs(controller.model.number_of_inputs+1:end); 
        end
        disp([ 'ipopt [' num2str(i) '/' num2str(number_of_steps) ']' 'The optimal input is[' num2str(optimal_input(1)) ' ; ' num2str(optimal_input(2)) ']']);
        
        state = controller.model.get_next_state_double(state, optimal_input)+((rand - 0.5)*2)*noise_amplitude;
        state_history(:, i) = state;
    end
    
    disp("Final state:")
    disp(state)
    
    clear('sim'); % remove the simulator so it unloads the shared lib
end
%initial_state,state_reference,input_reference,location
function [gradient] = gradient_f_multiarg(simulator,state,reference_state,reference_input,inputs_horizon)
    [cost,gradient] = simulator.evaluate_cost_gradient(...
            state,reference_state,reference_input,inputs_horizon);
end

