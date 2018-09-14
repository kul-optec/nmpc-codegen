function controller = prepare_demo_quadcopter( controller_folder_name,step_size,Q,R,Q_terminal,R_terminal )
%PREPARE_DEMO_CONTROLLER Prepare a controller 
%   Construct the controller from the quadcopter model and bootstrap the
%   enviroment. (output location is repo/test_controller_builds/controller_folder_name)

    % generate static files
    trailer_controller_output_location =  ['../../../test_controller_builds/' controller_folder_name];
    simulation_tools=true;
    nmpccodegen.tools.Bootstrapper.bootstrap(trailer_controller_output_location, simulation_tools);

    % get example model from lib
    [system_equations, number_of_states, number_of_inputs, coordinates_indices] ...
    = nmpccodegen.example_models.get_quadcopter_model();

    integrator = 'RK44';  % select a Runga-Kutta  integrator (FE is forward euler)
    constraint_input = nmpccodegen.Cfunctions.IndicatorBoxFunction([0, 0, 0, 0], [100, 100, 100, 100]);  % input needs stay within these borders
    model = nmpccodegen.models.Model_continuous(system_equations, constraint_input, step_size, number_of_states, ...
                                number_of_inputs, coordinates_indices, integrator);

    % define the controller
    stage_cost = nmpccodegen.controller.Stage_cost_QR(model, Q, R);
    terminal_cost = nmpccodegen.controller.Stage_cost_QR(model, Q_terminal, R_terminal);
    controller = nmpccodegen.controller.Nmpc_panoc(trailer_controller_output_location, model, stage_cost,terminal_cost);
end

