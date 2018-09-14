function [ available ] = Matlab_test_utils_test_if_command_available( command,pattern )
    % Test if a command is available by executing it and checking if it
    % contains a specific pattern
    % - command contains the command
    % -
    [~,cmdout] = system(command);
    available = ~isempty(strfind(cmdout,pattern));
end

