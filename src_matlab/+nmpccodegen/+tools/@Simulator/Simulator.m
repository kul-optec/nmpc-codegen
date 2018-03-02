classdef Simulator
    %SIMULATOR Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        nmpc_controller_location
    end
    
    methods
        function obj = Simulator(nmpc_controller_location)
            % Safety measure, if library is still loaded due to crash,
            % unload it irst.
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
            if libisloaded('nmpc_panoc')
                unloadlibrary('nmpc_panoc');
            end
        end
        function obj = make_build_system(obj)
            current_location = pwd; % save starting location
            cd(obj.nmpc_controller_location);
            if ismac
                !cmake .
            elseif isunix
                !cmake .
            elseif ispc
                !cmake . -G "MinGW Makefiles"
            else
                disp('Platform not supported');
            end
            cd(current_location); % go back to start location
        end
        function obj = compile_interface(obj)
            current_location = pwd;  % save starting location
            cd(obj.nmpc_controller_location);
            !make python_interface
            cd(current_location); % go back to start location
        end
        function obj = load_library(obj)
            if not(libisloaded('nmpc_panoc'))
                disp('Loading nmpc_panoc library \n');
                lib_file_name = [obj.nmpc_controller_location '/libpython_interface.dll'];
                lib_file_header_name = [obj.nmpc_controller_location '/libpython_interface.h'];
                
                [notfound,warnings] = loadlibrary(lib_file_name,lib_file_header_name,'alias','nmpc_panoc');
            end
        end
        function obj = nmpc_python_interface(obj)
        end
        function simulation_data = simulate_nmpc(obj,current_state,state_reference,input_reference)
            current_state_ = libpointer('doublePtr',current_state);
            state_reference_ = libpointer('doublePtr',state_reference);
            input_reference_ = libpointer('doublePtr',input_reference);
            
            optimal_inputs = zeros(1,length(input_reference));
            optimal_inputs_ = libpointer('doublePtr',optimal_inputs);
            
            [time_struct_pointer,~,~,~] = calllib('nmpc_panoc','simulate_nmpc_panoc',...
                current_state_,state_reference_,input_reference_,optimal_inputs_);
            
            simulation_data = nmpccodegen.tools.Simulation_data(time_struct_pointer, optimal_inputs_.value);
        end
        function set_weight_obstacle(obj,obstacle_id,weight)
            calllib('nmpc_panoc','simulation_set_weight_obstacles',int32(obstacle_id),weight);
        end
    end
    
end

