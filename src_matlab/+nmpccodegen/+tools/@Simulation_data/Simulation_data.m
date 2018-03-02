classdef Simulation_data
    %SIMULATION_DATA Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        optimal_input
        hours
        minutes
        seconds
        milli_seconds
        micro_seconds
        nano_seconds
        panoc_interations
        time_string
    end
    
    methods
        function obj = Simulation_data(time_struct_pointer,optimal_input)
            obj.optimal_input=optimal_input;
            
            obj.hours=time_struct_pointer.value.hours;
            obj.minutes=time_struct_pointer.value.minutes;
            obj.seconds=time_struct_pointer.value.seconds;

            obj.milli_seconds=time_struct_pointer.value.milli_seconds;
            obj.micro_seconds=time_struct_pointer.value.micro_seconds;
            obj.nano_seconds=time_struct_pointer.value.nano_seconds;
            
            obj.panoc_interations=time_struct_pointer.value.panoc_interations;
            
            obj.time_string = ['[' num2str(obj.hours) ':' num2str(obj.minutes) ':' num2str(obj.seconds) ']' ...
                '  [' num2str(obj.milli_seconds) ':' num2str(obj.micro_seconds) ':' num2str(obj.nano_seconds) ']'];
        end
    end
    
end

