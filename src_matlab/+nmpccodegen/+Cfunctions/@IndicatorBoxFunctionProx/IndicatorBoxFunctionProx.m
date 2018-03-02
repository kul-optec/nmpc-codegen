classdef IndicatorBoxFunctionProx <  nmpccodegen.Cfunctions.Cfunction
    %INDICATORBOXFUNCTION Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        lower_limits
        upper_limits
        dimension
    end
    
    methods
        function obj=IndicatorBoxFunctionProx(lower_limits,upper_limits)
            obj.lower_limits=lower_limits;
            obj.upper_limits=upper_limits;
            obj.dimension = min(length(lower_limits),length(upper_limits));
        end
        function obj=generate_c_code(obj,location)
            source_file = nmpccodegen.Cfunctions.Source_file_generator(location,'proxg');
            source_file = source_file.open();
            source_file = source_file.start_for('i','MPC_HORIZON',1);

            for i_dimension=1:obj.dimension
                source_file = source_file.write_comment_line(...
                    'check if the value of the border is outside the box, if so go to the nearest point inside the box',...
                    2);
                source_file = source_file.write_line(['if(state[' num2str(i_dimension) ']<' num2str(obj.lower_limits(i_dimension)) '){'],2);
                source_file = source_file.set_output(i_dimension,num2str(obj.lower_limits(i_dimension)),3);
                source_file = source_file.write_line(['}else if(state[' num2str(i_dimension) ']>' num2str(obj.upper_limits(i_dimension)) '){'] ,2);
                source_file = source_file.set_output(i_dimension, num2str(obj.upper_limits(i_dimension)), 3);
                source_file = source_file.write_line('}else{', 2);
                source_file = source_file.set_output(i_dimension,[ 'state[' num2str(i_dimension) ']'], 3);
                source_file = source_file.write_line('}', 2);
            end

            source_file = source_file.write_line(['state+=' num2str(obj.dimension) ';'],2);
            source_file = source_file.close_for(1);
            source_file.close();
        end
    end
    
end

