import os
from pathlib import Path
from shutil import copyfile
import platform

class Bootstrapper_panoc_nmpc:
    """bootstraps and nmpc enviroment"""
    def bootstrap(location_nmpc_repo,location,controller_name,python_interface_enabled):
        """ bootstrap the nmpc at location nmpc """
        print("GENERATING folders for controller:"+controller_name)
        Bootstrapper_panoc_nmpc._bootstrap_folders(location,controller_name)
        location_controller = location+"/"+controller_name

        overwrite = True
        print("GENERATING PANOC")
        Bootstrapper_panoc_nmpc._generate_PANOC_lib(\
            location+"/"+controller_name,location_nmpc_repo,overwrite)
        print("GENERATING static globals")
        Bootstrapper_panoc_nmpc._generate_static_globals(\
            location + "/" + controller_name, location_nmpc_repo,overwrite)
        if(python_interface_enabled):
            print("GENERATING python interface")
            Bootstrapper_panoc_nmpc._generate_python_interface(\
                location + "/" + controller_name, location_nmpc_repo,overwrite)
            print("GENERATING Build system")
            Bootstrapper_panoc_nmpc._generate_build_system(\
                location + "/" + controller_name, location_nmpc_repo,overwrite)
            # if all the files are there generate the make files using Cmake
            Bootstrapper_panoc_nmpc._make_build_system(location+"/"+controller_name)

    def _bootstrap_folders(location,controller_name):
        """ bootstrap the nmpc at location nmpc """
        lib_location = location + "/"+controller_name
        Bootstrapper_panoc_nmpc._create_folder_if_not_exist(lib_location)
        Bootstrapper_panoc_nmpc._create_folder_if_not_exist(lib_location+"/casadi")
        Bootstrapper_panoc_nmpc._create_folder_if_not_exist(lib_location + "/globals")
        Bootstrapper_panoc_nmpc._create_folder_if_not_exist(lib_location + "/include")
        Bootstrapper_panoc_nmpc._create_folder_if_not_exist(lib_location + "/PANOC")
        Bootstrapper_panoc_nmpc._create_folder_if_not_exist(lib_location + "/python_interface")
    def _generate_PANOC_lib(location,location_nmpc_repo,overwrite):
        src_files = ["buffer.c","buffer.h","casadi_definitions.h","lbfgs.h","lbfgs.c","lipschitz.c","lipschitz.h",\
                     "matrix_operations.h","matrix_operations.c","nmpc.c","panoc.c","panoc.h",\
                     "proximal_gradient_descent.c","proximal_gradient_descent.h","casadi_interface.c","casadi_interface.h"]

        for i in range(0,len(src_files)):
            src_location=location_nmpc_repo+"/panoc/"+src_files[i]
            dst_location = location + "/panoc/" + src_files[i]
            Bootstrapper_panoc_nmpc._copy_over_file(src_location,dst_location,overwrite)

        src_location = location_nmpc_repo + "/include/" + "nmpc.h"
        dst_location = location + "/include/" + "nmpc.h"
        Bootstrapper_panoc_nmpc._copy_over_file(src_location, dst_location, overwrite)

    def _generate_static_globals(location,location_nmpc_repo,overwrite):
        src_location = location_nmpc_repo + "/globals/" + "globals.h"
        dst_location = location + "/globals/" + "globals.h"
        Bootstrapper_panoc_nmpc._copy_over_file(src_location,dst_location,overwrite)

    def _generate_python_interface(location, location_nmpc_repo, overwrite):
        src_files = ["nmpc_python.c"]

        for i in range(0, len(src_files)):
            src_location = location_nmpc_repo + "/python_interface/" + src_files[i]
            dst_location = location + "/python_interface/" + src_files[i]
            Bootstrapper_panoc_nmpc._copy_over_file(src_location, dst_location, overwrite)

    def _generate_build_system(location,location_nmpc_repo,overwrite):
        src_location = location_nmpc_repo + "/minimum_build_system/" + "CMakeLists_root.txt"
        dst_location = location + "/CMakeLists.txt"
        Bootstrapper_panoc_nmpc._copy_over_file(src_location,dst_location,overwrite)

        src_location = location_nmpc_repo + "/minimum_build_system/" + "CMakeLists_panoc.txt"
        dst_location = location + "/panoc/" + "CMakeLists.txt"
        Bootstrapper_panoc_nmpc._copy_over_file(src_location, dst_location, overwrite)

    def _create_folder_if_not_exist(location):
        # check if the folder excists
        file = Path(location)
        if (file.exists()):
            print(location + ": folder already exists, leaving it in place")
        else:
            os.makedirs(location)
    def _copy_over_file(src_location,dst_location,overwrite):
        file = Path(src_location)
        if(file.exists()==False):
            print("ERROR: cannot find file: "+src_location)
        else:
            file = Path(dst_location)
            if (file.exists()):
                if(overwrite):
                    print(dst_location + ": file already exists, replacing it")
                    os.remove(dst_location)
                    copyfile(src_location, dst_location)
                else:
                    print(dst_location + ": file already exists, leaving it in place")
            else:
                copyfile(src_location, dst_location)

    def _make_build_system(location):
        cwd = os.getcwd()
        try:
            os.chdir(location)
            if (platform.system() == 'Linux'):
                os.system("cmake .")
            elif(platform.system() == 'Windows'):
                os.system("cmake . -G \"MinGW Makefiles\"")
            else:
                print("ERROR Platform not supported use either Linux or Windows")
        finally:
            os.chdir(cwd)