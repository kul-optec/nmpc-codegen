function trailer_controller = prepare_demo_trailer( controller_folder_name,step_size,Q,R,Q_terminal,R_terminal )
%PREPARE_DEMO_TRAILER Prepare a controller 
%   Construct the controller from the trailer model and bootstrap the
%   enviroment. (output location is repo/test_controller_builds/demo_controller_matlab)

    % generate static files
    trailer_controller_output_location =  ['../../test_controller_builds/' controller_folder_name];
    nmpccodegen.tools.Bootstrapper.bootstrap(trailer_controller_output_location, true);

    % get example model from lib
    [system_equations, number_of_states, number_of_inputs, coordinates_indices] ...
        = nmpccodegen.example_models.get_trailer_model(0.5);

    integrator = 'RK44';  % select a Runga-Kutta  integrator (FE is forward euler)
    constraint_input = nmpccodegen.Cfunctions.IndicatorBoxFunction([-4, -4], [4, 4]);  % input needs stay within these borders
    model = nmpccodegen.models.Model_continuous(system_equations, constraint_input, step_size, number_of_states, ...
                                    number_of_inputs, coordinates_indices, integrator);

    % define the controller
    stage_cost = nmpccodegen.controller.Stage_cost_QR(model, Q, R);
    terminal_cost = nmpccodegen.controller.Stage_cost_QR(model, Q_terminal, R_terminal);
    trailer_controller = nmpccodegen.controller.Nmpc_panoc(trailer_controller_output_location, model, stage_cost,terminal_cost);
end

