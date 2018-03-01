classdef Source_file_generator
    %SOURCE_FILE_OPERATIONS Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        location
        function_type
        source_file
    end
    methods
        function obj = Source_file_generator(location,function_type)
            obj.location=location;
            obj.function_type=function_type;
            obj.source_file=[];
        end
        function obj = open(obj)
            if (exist(obj.location)==2)
                disp([obj.location ' already exists, removing it before adding the new file']);
            end
            obj.source_file = fopen(obj.location, 'w');
            date_string = ['/* file generated on ' datestr(datetime('now')) ' in Matlab */ \n'];
            fprintf(obj.source_file,date_string);
            
            if (strcmp(obj.function_type,'g'))
                disp('generating g-type function');
                string = 'real_t casadi_interface_g(const real_t* state){\n';
                fprintf(obj.source_file,string);
            elseif (strcmp(obj.function_type,'proxg'))
                disp('generating proxg-type function')
                string= 'void casadi_interface_proxg(real_t* state){\n';
                fprintf(obj.source_file,string);
            else
                disp('ERROR wrong function_type pick either g or proxg');
                fclose(obj.source_file);
            end
        end
        function obj = start_for(obj,iterator_name,length,indent)
            obj.write_line(['size_t ' iterator_name ';'],indent)
            obj.write_line(['for(' iterator_name '=0;i<' length ';i++){' ],indent);
        end
        function obj = close_for(obj,indent)
            obj.write_line('}',indent);
        end
        function obj = write_line(obj,line,indent)
            string_indent = repmat(' ' , [1,indent*3]);
            string = [string_indent line '\n'];
            fprintf(obj.source_file,string);
        end
        function obj = write_define(obj,name,value,indent)
            obj.write_line(['#define ' name ' ' num2str(value)],indent);
        end
        function obj = write_comment_line(obj,line,indent)
            obj.write_line(['/* ' line ' */'],indent);
        end
        function obj = set_output(obj,output_index,value,indent)
            obj.write_line(['state[' num2str(output_index) ']=' num2str(value) ';'],indent);
        end
        function obj = close(obj)
            string = '\n}\n';
            fprintf(obj.source_file,string);
            fclose(obj.source_file);
        end
    end
    
end

