classdef Model
    %MODEL A discrete model describing the system behavior
    %   - If your model is continuous use the Model_continuous class.
    
    properties
        system_equations % The system equations, expressed as Matlab functions in the form f(state,input).
        input_constraint % The input constraints, must be a nmpccodegen.Cfunctions.ProximalFunction object.
        step_size % The step size of the indicator.
        number_of_states % The dimension of the state.
        number_of_inputs % The dimension of the input.
        indices_coordinates
    end
    
    methods
        function obj = Model(system_equations,input_constraint,step_size,...
                number_of_states,number_of_inputs,indices_coordinates)
            % Constructor of a discrete Model
            %   - system_equations: The dicrete system equations, expressed as Matlab
            %   functions in the form x_next = f(state,input).
            %   - input_constraint: The input constraints, must be a nmpccodegen.Cfunctions.ProximalFunction object.
            %   - step_size: The step size of the indicator.
            %   - number_of_states: The dimension of the state.
            %   - number_of_inputs: The dimension of the input.
            %   - indices_coordinates: 

            obj.system_equations=system_equations;
            obj.input_constraint=input_constraint;
            obj.step_size=step_size;
            obj.number_of_states=number_of_states;
            obj.number_of_inputs=number_of_inputs;
            obj.indices_coordinates=indices_coordinates;
        end
        function generate_constraint(obj,location)
            % used internally by Nmpc_panoc.generate_code()
            
            obj.input_constraint.generate_c_code([location '/casadi/g.c']);
            obj.input_constraint.prox.generate_c_code([location  '/casadi/proxg.c']);
        end
        function next_state = get_next_state(obj,state,input)
            % Get the next state of the system using the input and the
            % current state.
            
            next_state = obj.system_equations(state,input);
        end
        function next_state = get_next_state_double(obj,state,input)
            % Get the next state of the system using the input and the
            % current state in doubles and not in casadi variables.
            
            next_state_casadi = get_next_state(obj,state,input);
            next_state = double(full(next_state_casadi(1).evalf));
        end
    end
    
end

