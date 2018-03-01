classdef Casadi_code_generator
    %CASADI_CODE_GENERATOR Generates the casadi c code
    %   Detailed explanation goes here

    methods(Static)
        function [cost_function,cost_function_derivative_combined] = ...
                setup_casadi_functions_and_generate_c(static_casadi_parameters,input_all_steps,...
                obstacle_weights,cost,location_lib)

            cost_function = casadi.Function('cost_function', [static_casadi_parameters, input_all_steps,obstacle_weights], [cost]);
            cost_function_derivative_combined = casadi.Function('cost_function_derivative_combined',...
                                                            [static_casadi_parameters, input_all_steps,obstacle_weights],...
                                                            [cost, cd.gradient(cost, input_all_steps)]);

            Casadi_code_generator.translate_casadi_to_c(cost_function,location_lib, 'cost_function');
            Casadi_code_generator.translate_casadi_to_c(cost_function_derivative_combined,location_lib,...
                                                            'cost_function_derivative_combined');
        end
        
        function translate_casadi_to_c(casadi_function,location_lib,filename)
            % check if the buffer file excists, should never be the case, but check anyway
%             buffer_file_name='buffer.c';
%             if (exist(['./' buffer_file_name]))
%                  delete (['./' buffer_file_name]);
%             end
            
            % generate the casadi function in C to a buffer file
            opts =   struct('verbose',false,...
                            'mex',false,...
                            'cpp',false,...
                            'main',false,...
                            'codegen_scalars',false,...
                            'with_header',true,...              
                            'with_mem',false...
                            );

            casadi_function.generate(filename,opts);
            file_name_costfunction = [location_lib  '/casadi/' filename];

            % check if the files already exist
            if(exist([file_name_costfunction '.c']))
                disp([file_name_costfunction '.c' ' already exists: removing file...'])
                delete([file_name_costfunction '.c'])
            end

            if(exist([file_name_costfunction '.h']))
                disp([file_name_costfunction '.h' ' already exists: removing file...'])
                delete([file_name_costfunction '.h'])
            end

            movefile( [filename '.c'], [file_name_costfunction '.c']);
            movefile( [filename '.h'], [file_name_costfunction '.h']);
    
        end
    end
end

