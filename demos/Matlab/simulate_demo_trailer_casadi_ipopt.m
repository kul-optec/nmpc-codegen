function [ state_history,time_history ] = simulate_demo_trailer_casadi_ipopt( trailer_controller, ...
    initial_state,reference_state,reference_input,obstacle_weights,shift_horizon )
%SIMULATE_DEMO_TRAILER_PANOC_MATLAB Summary of this function goes here
%   Detailed explanation goes here
    % -- simulate controller --
    simulation_time = 3;
    number_of_steps = ceil(simulation_time / trailer_controller.model.step_size);    
    number_of_steps=20;
    %% ipopt specific stuff
    opt_ipopt.jit = true;
    opt_ipopt.jit_options.flags = {'-O'};
    opt_ipopt.jit_options.verbose = true;
%     opt_ipopt.compiler = 'shell';
%     opt_ipopt.jit_options.compiler = 'gcc';
    opt_ipopt.ipopt.hessian_approximation = 'limited-memory';
    opt_ipopt.ipopt.limited_memory_max_history = 50;
    opt_ipopt.ipopt.tol = 1e-10;
    opt_ipopt.ipopt.print_level = 3;
    opt_ipopt.print_time = false;
    
    %%
    inputs = repmat(zeros(trailer_controller.model.number_of_inputs, 1), ...
        trailer_controller.horizon, 1);
    
    %%
    state = initial_state;
    state_history = zeros(trailer_controller.model.number_of_states, number_of_steps);
    time_history = zeros(number_of_steps,1);
    iteration_history = zeros(number_of_steps,1);    
    
    for i=1:number_of_steps
        static_casadi_parameters = vertcat(initial_state, reference_state,reference_input);
        f_cost = @(x) trailer_controller.cost_function(static_casadi_parameters,x,obstacle_weights);
        x_max = 4;
        x_min = -4;
        
        x = casadi.SX.sym('x',trailer_controller.model.number_of_inputs*trailer_controller.horizon,1);
        nlp = struct('x',x,'f',f_cost(x));
        S = casadi.nlpsol('S','ipopt',nlp,opt_ipopt);
        
        to=tic;
        r = S('x0',inputs,'lbx',x_min,'ubx',x_max);% solve
        time_history(i)=toc(to)*1000;% get time in ms
        
        inputs = r.x; 
        iteration_history(i)=0;% not relevant put to zero
        
        optimal_input=full(inputs(1:trailer_controller.model.number_of_inputs));
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
    
end

