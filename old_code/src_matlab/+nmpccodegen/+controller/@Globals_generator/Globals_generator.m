classdef Globals_generator
    %GLOBALS_GENERATOR Generates the globals/globals_dyn.h  header file
    %   This class is used internally by the Nmpc_panoc class.
    
    properties
        location_globals % Where to generate the header file.
    end
    
    methods(Access = public)
        function obj = Globals_generator( location_globals)
            % Constructor of the Globals_generator class
            %   location_globals=location of the header file
            obj.location_globals=location_globals;
        end
        function generate_globals(obj,nmpc_controller)
            % Generated the header file at the location specified by the
            % construct.
            %   nmpc_controller : Controller object that contains the attributes
            %   used in generating the header file.
            disp(['Generating globals file at: ' obj.location_globals]);
            obj.init_globals_file();
            
            obj.generate_title('Problem specific definitions');
            obj.define_variable('DIMENSION_INPUT', num2str(nmpc_controller.model.number_of_inputs));
            obj.define_variable('DIMENSION_STATE', num2str(nmpc_controller.model.number_of_states));
            obj.define_variable('DIMENSION_PANOC', num2str(nmpc_controller.dimension_panoc));
            obj.define_variable('MPC_HORIZON', num2str(nmpc_controller.horizon));
            if(nmpc_controller.shift_input)
                obj.define_variable('SHIFT_INPUT', num2str(1));
            end
            
            obj.generate_title('Lagrangian related values, only visible if there are general constraints');
            if(~isempty(nmpc_controller.general_constraints))
                obj.define_variable('USE_LA', '1');
                obj.define_variable('NUMBER_OF_GENERAL_CONSTRAINTS', num2str(length(nmpc_controller.general_constraints)*nmpc_controller.horizon));
                obj.define_variable('NUMBER_OF_GENERAL_CONSTRAINTS_PER_STEP', num2str(length(nmpc_controller.general_constraints)));
                obj.define_variable('CONSTRAINT_OPTIMAL_VALUE', num2str(nmpc_controller.constraint_optimal_value));
                obj.define_variable('CONSTRAINT_MAX_WEIGHT', num2str(nmpc_controller.constraint_max_weight));
                obj.define_variable('START_RESIDUAL', num2str(nmpc_controller.start_residual));
                obj.define_variable('MAX_STEPS_LA', num2str(nmpc_controller.max_steps_LA));
            end

            obj.generate_title('Constraint related values');
            obj.define_variable('NUMBER_OF_CONSTRAINTS', ...
                num2str(nmpc_controller.get_number_of_constraints()) );
            obj.define_variable('DEFAULT_CONSTRAINT_WEIGHT', num2str(1));
            obj.set_data_type(nmpc_controller.data_type);

            obj.generate_title('lbgfs solver definitions');
            obj.define_variable('LBGFS_BUFFER_SIZE',num2str(nmpc_controller.lbgfs_buffer_size));

            obj.generate_title('NMPC-PANOC solver definitions');
            obj.define_variable('PANOC_MAX_STEPS',num2str(nmpc_controller.panoc_max_steps));
            obj.define_variable('PANOC_MIN_STEPS',num2str(nmpc_controller.panoc_min_steps));
            obj.define_variable('MIN_RESIDUAL',num2str(1e-3));
            
            obj.generate_title('options used to test:')
            if(nmpc_controller.pure_prox_gradient)
                obj.define_variable('PURE_PROX_GRADIENT',1);
            end

            obj.generate_title('Optional features');
            if( nmpc_controller.integrator_casadi)
                obj.define_variable('INTEGRATOR_CASADI',num2str(1));
            end
            
        end
    end
    methods(Access = private)
        function init_globals_file(obj)
            % Open the file stream to a new header file.
            fid = fopen(obj.location_globals,'w');

            date_string = ['/* file generated on ' datestr(datetime('now')) ' in Matlab */ \n'];
            fprintf(fid,date_string);
            
            fclose(fid);
        end
        function define_variable(obj,variable_name,variable_value)
            % Add a preprocessor defined to the header file.
            fid = fopen(obj.location_globals,'a');

            lines = ['#define ' variable_name ' ' variable_value '\n'];
            fprintf(fid,lines);
      
            fclose(fid);
        end
        function generate_comment(obj,comment)
            % Generate a one line comment.
            fid = fopen(obj.location_globals,'a');

            fprintf(fid,['/* ' comment ' */ \n']);

            fclose(fid);
        end
        function generate_title(obj,title)
            % Generate a title in comment existing out of a line then on the
            % net line the title followed by another line.
            fid = fopen(obj.location_globals,'a');

            fprintf(fid,['/*' '\n' '* ---------------------------------' '\n']);
            fprintf(fid,['* ' , title , '\n']);
            fprintf(fid,['* ---------------------------------' '\n' '*/' '\n']);

            fclose(fid);
        end
        function set_data_type(obj,data_type)
            % Set the datatype to either double or single precision.
            if(strcmp(data_type,'single precision'))
                obj.generate_title('constants used with float data type');
                obj.define_variable('real_t','float');
                obj.generate_comment('data types have different absolute value functions');
                obj.define_variable('ABS(x)', 'fabsf(x)');
                obj.generate_comment('Machine accuracy of IEEE float');
                obj.define_variable('MACHINE_ACCURACY', 'FLT_EPSILON');
                obj.generate_comment('large number use with things like indicator functions');
                obj.define_variable('LARGE', '100000');
            elseif(strcmp(data_type,'double precision'))
                obj.generate_title('constants used with double data type');
                obj.define_variable('real_t', 'double');
                obj.generate_comment('data types have different absolute value functions');
                obj.define_variable('ABS(x)', 'fabs(x)');
                obj.generate_comment('Machine accuracy of IEEE double');
                obj.define_variable('MACHINE_ACCURACY', 'DBL_EPSILON');
                obj.generate_comment('large number use with things like indicator functions');
                obj.define_variable('LARGE', '10000000000');
            else
                disp('Error: invalid data type, not supported by globals generator');
            end
        end
    end
    
end