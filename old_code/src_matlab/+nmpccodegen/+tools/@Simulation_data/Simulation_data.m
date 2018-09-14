classdef Simulation_data
    %SIMULATION_DATA results of a simulation.
    %   After the simulator simulates, it will return an
    %   object of this class.
    
    properties
        optimal_input % The optimal input that should be applied to the system.
        hours % The convergence time is the sum of hours/minutes/seconds/milli_seconds/micro_seconds/nano_seconds
        minutes % The convergence time is the sum of hours/minutes/seconds/milli_seconds/micro_seconds/nano_seconds
        seconds % The convergence time is the sum of hours/minutes/seconds/milli_seconds/micro_seconds/nano_seconds
        milli_seconds % The convergence time is the sum of hours/minutes/seconds/milli_seconds/micro_seconds/nano_seconds
        micro_seconds % The convergence time is the sum of hours/minutes/seconds/milli_seconds/micro_seconds/nano_seconds
        nano_seconds % The convergence time is the sum of hours/minutes/seconds/milli_seconds/micro_seconds/nano_seconds
        panoc_interations % The amount of iterations to convergence.
        time_string % The time till convergnce formatted as a string.
    end
    
    methods
        function obj = Simulation_data(time_struct_pointer,optimal_input)
            % constructor used internally by the Simulator class
            
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

