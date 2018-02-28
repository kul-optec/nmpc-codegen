classdef Model
    %MODEL a discrete model describing the system behavior
    %   Detailed explanation goes here
    
    properties
        system_equations
        input_constraint
        step_size
        number_of_states
        number_of_inputs
        indices_coordinates
    end
    
    methods
        function obj = Model(system_equations,input_constraint,step_size,...
                number_of_states,number_of_inputs,indices_coordinates)
            obj.system_equations=system_equations;
            obj.input_constraint=input_constraint;
            obj.step_size=step_size;
            obj.number_of_states=number_of_states;
            obj.number_of_inputs=number_of_inputs;
            obj.indices_coordinates=indices_coordinates;
        end
        function generate_constrain(obj,location)
            disp('TODO: Generating constraints at '+ location);
        end
        function next_state = get_next_state(obj,state,input)
            next_state = obj.system_equations(state,input);
        end
    end
    
end

