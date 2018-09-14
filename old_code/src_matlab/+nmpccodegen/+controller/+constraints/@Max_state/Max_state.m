classdef Max_state < nmpccodegen.controller.constraints.Constraint
    %MAX_STATE 
    %   A constraint needs at least the following function:
    %       - evaluate_cost , evaluates the cost of the constraint
    properties
        positions_state
        maximums_state
    end
    methods        
        function obj = Max_state(positions_state_,maximums_state_)
            % Constructs a Max_state constraint object:
            %    - positions_state: indices of states that are relevant to this
            %    constraint
            %    - maximums_state: the maximums of the absulute value of the relevant states
            obj.positions_state=positions_state_;
            obj.maximums_state=maximums_state_;
        end
        function cost = evaluate_cost(obj,state,input)
            % Evaluate the cost of the constraint, lowest possible cost is
            % zero.
            selected_states = state(obj.positions_state);
            
            % if the absolute value of the state is larger then the max,
            % punish !
            norm_difference_states = sum1(max(0,abs(selected_states) - obj.maximums_state).^2);
            
            cost = norm_difference_states;
        end
    end
end
