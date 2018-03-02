classdef Simulator
    %SIMULATOR Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        nmpc_controller_location
    end
    
    methods
        function obj = Simulator(nmpc_controller_location)
            obj.nmpc_controller_location=nmpc_controller_location;
            
            obj.make_build_system();
            obj.compile_interface();
            obj.load_library();
            calllib('nmpc_panoc','simulation_init');
        end
        function delete(obj)
            obj = obj.unload_library();
        end
        function obj = make_build_system(obj)
            disp('TODO implement call to cmake \n');
        end
        function obj = compile_interface(obj)
            disp('TODO implement call to make \n');
        end
        function obj = load_library(obj)
            if not(libisloaded('nmpc_panoc'))
                disp('Loading nmpc_panoc library \n');
                [notfound,warnings] = loadlibrary('./libpython_interface.dll','./libpython_interface.h','alias','nmpc_panoc');
            end
        end
        function obj = unload_library(obj)
            if libisloaded('nmpc_panoc')
                unloadlibrary('nmpc_panoc');
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
            
            simulation_data = Simulation_data(time_struct_pointer, optimal_inputs_.value);
        end
    end
    
end

