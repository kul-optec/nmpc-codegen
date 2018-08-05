function [ system_equations, number_of_states, number_of_inputs, coordinates_indices ] = get_quadcopter_model(  )
%GET_QUADCOPTER_MODEL Get the parameters required to build a model of a
%quadcopter.
% Return parameters:
%   system_equations : system equation in the form x_dot = f(x,u)
%   number_of_states : number of states
%   number_of_inputs : number of inputs

    number_of_states=12;
    number_of_inputs=4;
    coordinates_indices=[1;2;3];

    params.mass_quadcopter=0.5;
    params.radius_quadcopter=0.25;
    params.propeller_lift_coefficient=3e-6;
    params.propeller_drag_coefficient=1e-7;
    params.gravity_acceleration=9.81;
    params.air_friction_coefficient=0.25;
    params.quadcopter_initeria_x_axis=5e-3;
    params.quadcopter_initeria_y_axis=5e-3;
    params.quadcopter_initeria_z_axis=1e-2;
    params.motor_constant=1e4;

    system_equations = @(state,input) nmpccodegen.example_models.quadcopter_dyn(params,state,input);
end

