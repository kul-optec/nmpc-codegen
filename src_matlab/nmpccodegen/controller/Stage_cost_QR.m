classdef Stage_cost_QR
    %STAGE_COST Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        Q
        R
        model
    end
    
    methods
        function obj = Stage_cost_QR(Q,R)
            obj.Q=Q;
            obj.R=R;
            obj.model=model;
        end
        function stage_cost=evaluate_cost(obj,state,input,iteration_index,...
                state_reference,input_reference)
            stage_cost=0;

            for i_col=1:obj.model.number_of_states
                for i_row=1:obj.model.number_of_states
                    stage_cost = stage_cost + (state(i_col)-state_reference(i_col))*...
                                obj.Q(i_col,i_row)*...
                                (state(i_row)-state_reference(i_row));
                end
            end

            for i_col=1:obj.model.number_of_inputs
                for i_row=1:obj.model.number_of_inputs
                    stage_cost = stage_cost + (input(i_col)-input_reference(i_col))*...
                                obj.R(i_col,i_row)*...
                                (input(i_row)-input_reference(i_row));
                end
            end
        end
    end
    
end

