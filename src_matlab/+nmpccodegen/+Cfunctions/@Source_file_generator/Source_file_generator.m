classdef Source_file_generator
    %SOURCE_FILE_GENERATOR A class that helps you to easily generate C code functions.
    %   An example of the usage of this class is nmpccodegen.Cfunctions.IndicatorBoxFunction .
    
    properties(Access=private)
        source_file % File ID steam.
    end
    properties
        location % Location of the source file.
        function_type %  The function type they should be either 'g' or 'proxg'
    end
    methods
        function obj = open(obj)
            % Open the file stream, this function should be called before
            % doing any kind of file operation. 
            %   - The file stream can be closed again with the close function.
            
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
        function obj = close(obj)
            % Close the file stream, this function should be called after
            % all the file operations are executed.
            string = '\n}\n';
            fprintf(obj.source_file,string);
            fclose(obj.source_file);
        end
        function obj = Source_file_generator(location,function_type)
            % location = Location of the source file.
            % function_type =  The function type they should be either 'g' or 'proxg'
        
            obj.location=location;
            obj.function_type=function_type;
            obj.source_file=[];
        end
        function obj = start_for(obj,iterator_name,length,indent)
            % Start a for loop: for(iterator_name=0;i<length;i++){
            %   - indent : Amount of tabs used in front of the line.
            obj.write_line(['size_t ' iterator_name ';'],indent)
            obj.write_line(['for(' iterator_name '=0;i<' length ';i++){' ],indent);
        end
        function obj = close_for(obj,indent)
            % Close the for loop.
            %   - indent : Amount of tabs used in front of the line.
            obj.write_line('}',indent);
        end
        function obj = write_line(obj,line,indent)
            % Write a single line to the source file.
            %   - line :  string that contains the line that should be written
            %   to the source file.
            %   - indent : Amount of tabs used in front of the line.
            string_indent = repmat(' ' , [1,indent*3]);
            string = [string_indent line '\n'];
            fprintf(obj.source_file,string);
        end
        function obj = write_define(obj,name,value,indent)
            % Write a preprocessor defined to the source file.
            %   - name : Name of the preprocessor variable
            %   - value : Value of the variable, expressed as a number.
            %   - indent : Amount of tabs used in front of the line.
            obj.write_line(['#define ' name ' ' num2str(value)],indent);
        end
        function obj = write_comment_line(obj,line,indent)
            % Write a single line comment to the source file
            %   - line : The comment expressed as a string.
            %   - indent : Amount of tabs used in front of the line.
            obj.write_line(['/* ' line ' */'],indent);
        end
        function obj = set_output(obj,output_index,value,indent)
            % Set one value of the output to a specific value. (output[output_index]=value)
            %   - output_index : Index of the output arrays.
            %   - value : Value to set the output at a particular index.
            %   - indent : Amount of tabs used in front of the line.
            obj.write_line(['state[' num2str(output_index) ']=' num2str(value) ';'],indent);
        end
        
    end
    
end

