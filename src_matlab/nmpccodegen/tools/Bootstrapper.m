classdef Bootstrapper
    %BOOTSTRAPPER bootstraps static files of a controller
    %   output_location_controller: Folder where the controller files will be located
    %   simululation_tools: Enable this if you want to use the simulator
    %       class this will provide the nessary build system and src files
    %       to simulate.
    methods(Static)
        function bootstrap(output_location_controller,simulation_tools)
            location_nmpc_repo = Bootstrapper.get_repo_location();
            disp('GENERATING output folders of controller:')
            Bootstrapper.bootstrap_folders(output_location_controller);

            overwrite = true;
            disp('GENERATING PANOC')
            Bootstrapper.generate_PANOC_lib(output_location_controller,location_nmpc_repo,overwrite)
            disp('GENERATING static globals')
            Bootstrapper.generate_static_globals(output_location_controller, location_nmpc_repo,overwrite)

            if(simulation_tools)
                disp('GENERATING python interface')
                Bootstrapper.generate_python_interface(output_location_controller, location_nmpc_repo,overwrite)
                disp('GENERATING Build system')
                Bootstrapper.generate_build_system(output_location_controller, location_nmpc_repo,overwrite)
            end
        end
        function location_repo = get_repo_location()
            Folder = cd;
            relative_location_windows = '\src_matlab\nmpccodegen\tools';
            relative_location_unix = '\src_matlab\nmpccodegen\tools';
            Folder = strrep(Folder,relative_location_windows,'');
            Folder = strrep(Folder,relative_location_unix,'');
            location_repo = Folder;
        end
        function bootstrap_folders(lib_location)
            Bootstrapper.create_folder_if_not_exist(lib_location)
        	Bootstrapper.create_folder_if_not_exist([lib_location  '/casadi'])
        	Bootstrapper.create_folder_if_not_exist([lib_location  '/globals'])
        	Bootstrapper.create_folder_if_not_exist([lib_location  '/include'])
        	Bootstrapper.create_folder_if_not_exist([lib_location  '/PANOC'])
        	Bootstrapper.create_folder_if_not_exist([lib_location  '/python_interface'])
        end
        function generate_PANOC_lib(location,location_nmpc_repo,overwrite)
            src_files = {'buffer.c';'buffer.h';'casadi_definitions.h';...
                         'lbfgs.h';'lbfgs.c';'lipschitz.c';'lipschitz.h';...
                         'matrix_operations.h';'matrix_operations.c';'nmpc.c';'panoc.c';'panoc.h';...
                         'proximal_gradient_descent.c';'proximal_gradient_descent.h';...
                         'casadi_interface.c';'casadi_interface.h'};
            number_of_src_files = size(src_files,1);

            for i=1:number_of_src_files
                src_location=[ location_nmpc_repo '/PANOC/' src_files{i}];
                dst_location =[ location '/PANOC/' src_files{i} ];
                Bootstrapper.copy_over_file(src_location,dst_location,overwrite);
            end

            src_location = [ location_nmpc_repo '/include/' 'nmpc.h' ];
            dst_location = [ location  '/include/' 'nmpc.h'];
            Bootstrapper.copy_over_file(src_location, dst_location, overwrite);
        end

        function generate_static_globals(location,location_nmpc_repo,overwrite)
            src_location = [location_nmpc_repo '/globals/' 'globals.h'];
            dst_location = [location '/globals/' 'globals.h'];
            Bootstrapper.copy_over_file(src_location,dst_location,overwrite);
        end

        function generate_python_interface(location, location_nmpc_repo, overwrite)
            src_files = {'nmpc_python.c','timer.h','timer_linux.c','timer_windows.c'};
            number_of_src_files = size(src_files,1);
            
            for i=1:number_of_src_files
                src_location=[ location_nmpc_repo '/python_interface/' src_files{i}];
                dst_location =[ location '/python_interface/' src_files{i} ];
                Bootstrapper.copy_over_file(src_location,dst_location,overwrite);
            end
        end

        function generate_build_system(location,location_nmpc_repo,overwrite)
            src_location = [location_nmpc_repo '/minimum_build_system/' 'CMakeLists_root.txt'];
            dst_location = [location  '/CMakeLists.txt'];
            Bootstrapper.copy_over_file(src_location,dst_location,overwrite);

            src_location = [location_nmpc_repo '/minimum_build_system/' 'CMakeLists_panoc.txt'];
            dst_location = [location '/PANOC/' 'CMakeLists.txt'];
            Bootstrapper.copy_over_file(src_location, dst_location, overwrite)

            src_location = [location_nmpc_repo '/minimum_build_system/' 'CMakeLists_casadi.txt'];
            dst_location = [location '/casadi/' 'CMakeLists.txt'];
            Bootstrapper.copy_over_file(src_location, dst_location, overwrite)
        end

        function create_folder_if_not_exist(location)
            test = exist(location);
            if(test==7 )
                string = [location ': folder already exists, leaving it in place' ];
                disp(string);
            else
                mkdir(location);
            end
        end

        function copy_over_file(src_location,dst_location,overwrite)
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

