classdef IndicatorBoxFunction < nmpccodegen.Cfunctions.ProximalFunction
    %INDICATORBOXFUNCTION An indicator Box function that can be used as
    %input constraint.
    %   - 
    
    properties
        lower_limits %  the lower limits of the box.
        upper_limits % The upper limits of the box.
        dimension % Dimension of the box, this is equal to the length of the array's lower_limits and upper_limits.
    end
    
    methods
        function obj=IndicatorBoxFunction(lower_limits,upper_limits)
            % lower_limits :  the lower limits of the box.
            % upper_limits : The upper limits of the box.
            
            obj.lower_limits=lower_limits;
            obj.upper_limits=upper_limits;
            obj.dimension = min(length(lower_limits),length(upper_limits));
            
            obj.prox =  nmpccodegen.Cfunctions.IndicatorBoxFunctionProx(lower_limits,upper_limits);
        end
        function obj=generate_c_code(obj, location)
            % Generate the C code at the folder sepcified in location.
            
            source_file = nmpccodegen.Cfunctions.Source_file_generator(location,'g');
            source_file = source_file.open();
            source_file = source_file.start_for('i','MPC_HORIZON',1);
            
            for i_dimension=1:obj.dimension
                source_file.write_comment_line('check if the value of the border is outside the box, if so return zero', ...
                                               2);
                source_file = source_file.write_line( ['if(state[' num2str(i_dimension-1) ...
                    ']<' num2str(obj.lower_limits(i_dimension)) ...
                    ' || state[' num2str(i_dimension-1) ']>' ... 
                    num2str(obj.upper_limits(i_dimension))  ...
                    '){'],2);
                source_file = source_file.write_line('return LARGE;',3);
                source_file = source_file.write_line('}',2);
            end
            
            source_file = source_file.write_line(['state+=' num2str(obj.dimension) ';'],2);
            source_file = source_file.close_for(1);

            source_file = source_file.write_comment_line('if the values where never outside the box, return zero',1);
            source_file = source_file.write_line( 'return 0;', 1);
            source_file.close();
        end
    end
    
end