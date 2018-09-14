function [system_equations, number_of_states, number_of_inputs, coordinates_indices] = get_trailer_model( L )
%GET_TRAILER_MODEL Summary of this function goes here
%   Detailed explanation goes here
    number_of_states=3;
    number_of_inputs=2;
    coordinates_indices = [1 2]; % only x and y are coordinates, theta has nothing to do with position of the trailer
    system_equations = @(x,u) nmpccodegen.example_models.trailer_dyn(L,x,u);
end

