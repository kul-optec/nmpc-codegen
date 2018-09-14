classdef Bootstrapper
    %BOOTSTRAPPER Bootstraps static files of a controller
    %   output_location_controller: Folder where the controller files will be located
    %   simululation_tools: Enable this if you want to use the simulator
    %       class this will provide the nessary build system and src files
    %       to simulate.
    methods(Static)
        function bootstrap(output_location_controller,simulation_tools)
            % Create a folder that contains all the static files needed to
            % create a controller.
            %   - output_location_controller = Output location of the folder.
            %   - simulation_tools = Should be set on true if you want
            %   to use the simulator. If set on false, the bootstrapper
            %   will only provide the absolute minimum files to create a
            %   controller. 
            
            location_nmpc_repo = nmpccodegen.tools.Bootstrapper.get_repo_location();
            disp('GENERATING output folders of controller:')
            nmpccodegen.tools.Bootstrapper.bootstrap_folders(output_location_controller);

            overwrite = true;
            disp('GENERATING PANOC')
            nmpccodegen.tools.Bootstrapper.generate_PANOC_lib(output_location_controller,location_nmpc_repo,overwrite)
            disp('GENERATING static globals')
            nmpccodegen.tools.Bootstrapper.generate_static_globals(output_location_controller, location_nmpc_repo,overwrite)

            if(simulation_tools)
                disp('GENERATING python interface')
                nmpccodegen.tools.Bootstrapper.generate_python_interface(output_location_controller, location_nmpc_repo,overwrite)
                disp('GENERATING Build system')
                nmpccodegen.tools.Bootstrapper.generate_build_system(output_location_controller, location_nmpc_repo,overwrite)
            end
        end
    end
    methods(Static,Access = private)
        function location_repo = get_repo_location()
            % Get location of the library.
            
            Folder = which('nmpccodegen.tools.Bootstrapper');
            relative_location_windows = '\src_matlab\+nmpccodegen\+tools\@Bootstrapper\Bootstrapper.m';
            relative_location_unix = '/src_matlab/+nmpccodegen/+tools/@Bootstrapper/Bootstrapper.m';
            Folder = strrep(Folder,relative_location_windows,'');
            Folder = strrep(Folder,relative_location_unix,'');
            location_repo = Folder;
        end
        function bootstrap_folders(lib_location)
            % Create the folder structure if it doesn t exist yet.
            
            nmpccodegen.tools.Bootstrapper.create_folder_if_not_exist(lib_location)
        	nmpccodegen.tools.Bootstrapper.create_folder_if_not_exist([lib_location  '/casadi'])
        	nmpccodegen.tools.Bootstrapper.create_folder_if_not_exist([lib_location  '/globals'])
        	nmpccodegen.tools.Bootstrapper.create_folder_if_not_exist([lib_location  '/include'])
        	nmpccodegen.tools.Bootstrapper.create_folder_if_not_exist([lib_location  '/PANOC'])
        	nmpccodegen.tools.Bootstrapper.create_folder_if_not_exist([lib_location  '/python_interface'])
        end
        function generate_PANOC_lib(location,location_nmpc_repo,overwrite)
            % Puppy over the panoc algorithm.
            
            src_files = {'buffer.c';'buffer.h';'casadi_definitions.h';...
                         'lbfgs.h';'lbfgs.c';'lipschitz.c';'lipschitz.h';...
                         'matrix_operations.h';'matrix_operations.c';'nmpc.c';'panoc.c';'panoc.h';...
                         'proximal_gradient_descent.c';'proximal_gradient_descent.h';...
                         'casadi_interface.c';'casadi_interface.h'};
            number_of_src_files = size(src_files,1);

            for i=1:number_of_src_files
                src_location=[ location_nmpc_repo '/PANOC/' src_files{i}];
                dst_location =[ location '/PANOC/' src_files{i} ];
                nmpccodegen.tools.Bootstrapper.copy_over_file(src_location,dst_location,overwrite);
            end

            src_location = [ location_nmpc_repo '/include/' 'nmpc.h' ];
            dst_location = [ location  '/include/' 'nmpc.h'];
            nmpccodegen.tools.Bootstrapper.copy_over_file(src_location, dst_location, overwrite);
        end

        function generate_static_globals(location,location_nmpc_repo,overwrite)
            % Copy over the static globals file.
            
            src_location = [location_nmpc_repo '/globals/' 'globals.h'];
            dst_location = [location '/globals/' 'globals.h'];
            nmpccodegen.tools.Bootstrapper.copy_over_file(src_location,dst_location,overwrite);
        end

        function generate_python_interface(location, location_nmpc_repo, overwrite)
            % At the source files of the dynamic library used by the
            % simulator.
            
            src_files = {'nmpc_python.c','nmpc_python.h','timer.h','timer_linux.c','timer_windows.c','timer_mac.c'};
            number_of_src_files = size(src_files,2);
            
            for i=1:number_of_src_files
                src_location=[ location_nmpc_repo '/python_interface/' src_files{i}];
                dst_location =[ location '/python_interface/' src_files{i} ];
                nmpccodegen.tools.Bootstrapper.copy_over_file(src_location,dst_location,overwrite);
            end
            
            % copy over the header file matlab needs
            src_location=[ location_nmpc_repo '/python_interface' '/libpython_interface.h'];
            dst_location =[ location  '/libpython_interface.h'];
            nmpccodegen.tools.Bootstrapper.copy_over_file(src_location,dst_location,overwrite);
        end

        function generate_build_system(location,location_nmpc_repo,overwrite)
            % Copy over the cmake files.
            
            src_location = [location_nmpc_repo '/minimum_build_system/' 'CMakeLists_root.txt'];
            dst_location = [location  '/CMakeLists.txt'];
            nmpccodegen.tools.Bootstrapper.copy_over_file(src_location,dst_location,overwrite);

            src_location = [location_nmpc_repo '/minimum_build_system/' 'CMakeLists_panoc.txt'];
            dst_location = [location '/PANOC/' 'CMakeLists.txt'];
            nmpccodegen.tools.Bootstrapper.copy_over_file(src_location, dst_location, overwrite)

            src_location = [location_nmpc_repo '/minimum_build_system/' 'CMakeLists_casadi.txt'];
            dst_location = [location '/casadi/' 'CMakeLists.txt'];
            nmpccodegen.tools.Bootstrapper.copy_over_file(src_location, dst_location, overwrite)
        end

        function create_folder_if_not_exist(location)
            % Create a folder if it doesn t exist yet at location, if the
            % folder exists leave it in place.
            test = exist(location);
            if(test==7 )
                string = [location ': folder already exists, leaving it in place' ];
                disp(string);
            else
                mkdir(location);
            end
        end

        function copy_over_file(src_location,dst_location,overwrite)
            % Copy over a file from src_location to dst_location.
            %   - If overwrite is true the existing file will be
            %   overwritten.
            
            test = exist(dst_location);
            if(test==2 )
                if(overwrite)
                    string = [dst_location ': file already exists, replacing it' ];
                    delete(dst_location);
                    copyfile(src_location, dst_location, 'f');
                else
                    string = [dst_location ': file already exists, leaving it in place' ];
                end
                disp(string);
            else
                copyfile(src_location, dst_location, 'f');
            end
        end  
    end 
end

