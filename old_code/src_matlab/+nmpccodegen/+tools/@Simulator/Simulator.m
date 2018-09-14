classdef Simulator
    %SIMULATOR Simulates the controller by compiling the C code into a
    %dynamic library, and loading it into Matlab
    %   The simulator only works if the simulation tools were enabled when
    %   bootstrapping the environment.
    
    properties
        nmpc_controller_location % The location of the controller source code.
        visual_studio=false;
        debug=false;
    end
    methods(Static)
        function force_unload()
            % Unload the dynamic library if it is loaded.
            if libisloaded('nmpc_panoc')
                unloadlibrary('nmpc_panoc');
            end
        end
    end
    methods(Access=private)
        function obj = make_build_system(obj)
            % Call Cmake to construct the build system.
            current_location = pwd; % save starting location
            cd(obj.nmpc_controller_location);
            if ismac
                !cmake -H. -Bbuild
            elseif isunix
                !cmake -H. -Bbuild
            elseif ispc
                if(obj.visual_studio)
                    !cmake -H. -Bbuild -DCMAKE_GENERATOR_PLATFORM=x64
                else
                    !cmake -H. -Bbuild -G "MinGW Makefiles"
                end
            else
                disp('Platform not supported');
            end
            cd(current_location); % go back to start location
        end
        function obj = compile_interface(obj)
            % Call cmake to compile the dynamic library.
            current_location = pwd; % save starting location
            cd(obj.nmpc_controller_location);
            
            if(obj.debug)
                !cmake --build ./build --config Debug --target python_interface
            else
                !cmake --build ./build --config Release --target python_interface
            end
            
            cd(current_location); % go back to start location
        end
        function obj = load_library(obj)
            % Loads the dynamic library.
            
            extension='dll';
            if ismac
                extension= 'dylib'; % .dylib is dynamic one
            elseif isunix
                extension='so';
            end
            if not(libisloaded('nmpc_panoc'))
                disp('Loading nmpc_panoc library \n');
                lib_file_location= [obj.nmpc_controller_location '/build'];
                if(obj.visual_studio)
                    if(obj.debug)
                        lib_file_name = [lib_file_location '/Debug/python_interface.dll'];
                    else
                        lib_file_name = [lib_file_location '/Release/python_interface.dll'];
                    end
                else
                    lib_file_name = [lib_file_location '/libpython_interface.' extension];
                end
                
                lib_file_header_name = [obj.nmpc_controller_location '/libpython_interface.h'];
                
                [notfound,warnings] = loadlibrary(lib_file_name,lib_file_header_name,'alias','nmpc_panoc');
            end
        end
    end
    methods
        function obj = Simulator(nmpc_controller_location,option)
            % nmpc_controller_location = The location of the controller source code.
            if(nargin>1)
               if(strcmp(option,'visual studio')) 
                   obj.visual_studio=true;
               end
               if(strcmp(option,'visual studio debug')) 
                   obj.visual_studio=true;
                   obj.debug=true;
               end
            end
            
            % Safety measure, if library is still loaded due to crash,
            % unload it first.
            if libisloaded('nmpc_panoc')
                unloadlibrary('nmpc_panoc');
            end
            
            obj.nmpc_controller_location=nmpc_controller_location;
            
            obj.make_build_system();
            obj.compile_interface();
            obj.load_library();
            calllib('nmpc_panoc','simulation_init');
        end
        function delete(obj)
            %  unload the dynamic library if it is loaded.
            if libisloaded('nmpc_panoc')
                unloadlibrary('nmpc_panoc');
            end
        end
        function simulation_data = simulate_nmpc(obj,current_state,state_reference,input_reference)
            % Calculate the optimal inputs using the current state, the
            % reference state and the reference input.
            
            optimal_inputs = zeros(1,length(input_reference));
            optimal_inputs_ = libpointer('doublePtr',optimal_inputs);
            
            [time_struct_pointer,~,~,~] = calllib('nmpc_panoc','simulate_nmpc_panoc',...
                current_state,state_reference,input_reference,optimal_inputs_);
            
            simulation_data = nmpccodegen.tools.Simulation_data(time_struct_pointer, optimal_inputs_.value);
        end
        function [f_value,f_gradient] = evaluate_cost_gradient(obj,initial_state,state_reference,input_reference,location)
            % Evaluate the cost and the gradient of the optimal control
            % problem.
            
            static_casadi_parameters = vertcat(initial_state, state_reference,input_reference);
            
            gradient = zeros(size(location));
            gradient_ = libpointer('doublePtr',gradient);
            
            [f_value,~,~,~] = calllib('nmpc_panoc','simulation_evaluate_f_df',...
                static_casadi_parameters,location,gradient_);
            
            f_gradient = gradient_.value;
        end
        function [f_value] = evaluate_cost(obj,initial_state,state_reference,input_reference,location)
            % Evaluate the cost function of the optimal control problem.
            
            static_casadi_parameters = vertcat(initial_state, state_reference,input_reference);
            
            [f_value] = calllib('nmpc_panoc','simulation_evaluate_f',...
                static_casadi_parameters,location);
        end
        function set_weight_constraint(obj,constraint_id,weight)
            % Set the weight of an constraint to an different weight than the
            % default value.
            
            calllib('nmpc_panoc','simulation_set_weight_constraints',int32(constraint_id),weight);
        end
    end
    
end

