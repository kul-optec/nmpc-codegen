% Run this script to see if you dependencies are ok
disp('This script will check if the nessesary tools are available');

try
    version_casadi = casadi.CasadiMeta.version();
catch
    error('casadi version unavailable: unsupported casadi version');
end
version_split = strsplit(version_casadi,'.');
major_version = cell2mat(version_split(1));
minor_version = cell2mat(version_split(2));
if((major_version<3) || (major_version==3 && minor_version<2))
    disp('unsupported casadi version, install 3.2.x or higher');
else
    disp(['casadi version ' version_casadi '[OK]']);
end

command = 'gcc';
pattern = 'no input files';
if(test_if_command_available(command,pattern))
    disp('GNU compiler [OK]');
else
    disp('Error the GNU compiler is not available [NOT OK]');
end

command='make foobar';
pattern = 'No rule to make target `foobar';
if(test_if_command_available(command,pattern))
    disp('make [OK]');
else
    disp('Error the make is not available [NOT OK]');
end

command='cmake --help';
pattern='Specify a source directory';
if(test_if_command_available(command,pattern))
    disp('cmake [OK]');
else
    disp('Error cmake is not available [NOT OK]');
end

% Test if a command is available by executing it and checking if it
% contains a specific pattern
% - command contains the command
% -
function [available] = test_if_command_available(command,pattern)
    [~,cmdout] = system(command);
    available = ~isempty(strfind(cmdout,pattern));
end