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
if(Matlab_test_utils_test_if_command_available(command,pattern))
    disp('GNU compiler [OK]');
else
    disp('Error the GNU compiler is not available [NOT OK]');
end

command='make foobar';
pattern = 'No rule to make target `foobar';
if(Matlab_test_utils_test_if_command_available(command,pattern))
    disp('make [OK]');
else
    disp('Error the make is not available [NOT OK]');
end

command='cmake --help';
pattern='Specify a source directory';
if(Matlab_test_utils_test_if_command_available(command,pattern))
    disp('cmake [OK]');
else
    disp('Error cmake is not available [NOT OK]');
end