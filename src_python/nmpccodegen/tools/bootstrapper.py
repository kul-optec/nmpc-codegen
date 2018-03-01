import os
from pathlib import Path
from shutil import copyfile
import platform

import sys


class Bootstrapper:
    """ bootstraps an nmpc environment """
    def bootstrap(output_location_controller,simulation_tools=False):
        location_nmpc_repo = Bootstrapper._get_repo_location()
        """ bootstrap the nmpc at location nmpc """
        print("GENERATING output folders of controller:")
        Bootstrapper._bootstrap_folders(output_location_controller)

        overwrite = True
        print("GENERATING PANOC")
        Bootstrapper._generate_PANOC_lib(output_location_controller,location_nmpc_repo,overwrite)
        print("GENERATING static globals")
        Bootstrapper._generate_static_globals(output_location_controller, location_nmpc_repo,overwrite)
        if(simulation_tools):
            print("GENERATING python interface")
            Bootstrapper._generate_python_interface(output_location_controller, location_nmpc_repo,overwrite)
            print("GENERATING Build system")
            Bootstrapper._generate_build_system(output_location_controller, location_nmpc_repo,overwrite)

    @staticmethod
    def _get_repo_location():
        """ finds out where the lib is installed """
        bootstrapper_location = os.path.dirname(os.path.realpath(__file__))
        repo_location = os.path.dirname(os.path.dirname(os.path.dirname(bootstrapper_location)))

        return repo_location

    @staticmethod
    def _bootstrap_folders(lib_location):
        """ bootstrap the nmpc at location nmpc """
        Bootstrapper._create_folder_if_not_exist(lib_location)
        Bootstrapper._create_folder_if_not_exist(lib_location+"/casadi")
        Bootstrapper._create_folder_if_not_exist(lib_location + "/globals")
        Bootstrapper._create_folder_if_not_exist(lib_location + "/include")
        Bootstrapper._create_folder_if_not_exist(lib_location + "/PANOC")
        Bootstrapper._create_folder_if_not_exist(lib_location + "/python_interface")

    @staticmethod
    def _generate_PANOC_lib(location,location_nmpc_repo,overwrite):
        src_files = ["buffer.c","buffer.h","casadi_definitions.h","lbfgs.h","lbfgs.c","lipschitz.c","lipschitz.h",\
                     "matrix_operations.h","matrix_operations.c","nmpc.c","panoc.c","panoc.h",\
                     "proximal_gradient_descent.c","proximal_gradient_descent.h","casadi_interface.c","casadi_interface.h"]

        for i in range(0,len(src_files)):
            src_location=location_nmpc_repo+"/PANOC/"+src_files[i]
            dst_location = location + "/PANOC/" + src_files[i]
            Bootstrapper._copy_over_file(src_location,dst_location,overwrite)

        src_location = location_nmpc_repo + "/include/" + "nmpc.h"
        dst_location = location + "/include/" + "nmpc.h"
        Bootstrapper._copy_over_file(src_location, dst_location, overwrite)

    @staticmethod
    def _generate_static_globals(location,location_nmpc_repo,overwrite):
        src_location = location_nmpc_repo + "/globals/" + "globals.h"
        dst_location = location + "/globals/" + "globals.h"
        Bootstrapper._copy_over_file(src_location,dst_location,overwrite)

    @staticmethod
    def _generate_python_interface(location, location_nmpc_repo, overwrite):
        src_files = ["nmpc_python.c","timer.h","timer_linux.c","timer_windows.c"]

        for i in range(0, len(src_files)):
            src_location = location_nmpc_repo + "/python_interface/" + src_files[i]
            dst_location = location + "/python_interface/" + src_files[i]
            Bootstrapper._copy_over_file(src_location, dst_location, overwrite)

    @staticmethod
    def _generate_build_system(location,location_nmpc_repo,overwrite):
        src_location = location_nmpc_repo + "/minimum_build_system/" + "CMakeLists_root.txt"
        dst_location = location + "/CMakeLists.txt"
        Bootstrapper._copy_over_file(src_location,dst_location,overwrite)

        src_location = location_nmpc_repo + "/minimum_build_system/" + "CMakeLists_panoc.txt"
        dst_location = location + "/PANOC/" + "CMakeLists.txt"
        Bootstrapper._copy_over_file(src_location, dst_location, overwrite)

        src_location = location_nmpc_repo + "/minimum_build_system/" + "CMakeLists_casadi.txt"
        dst_location = location + "/casadi/" + "CMakeLists.txt"
        Bootstrapper._copy_over_file(src_location, dst_location, overwrite)

    @staticmethod
    def _create_folder_if_not_exist(location):
        # check if the folder excists
        file = Path(location)
        if (file.exists()):
            print(location + ": folder already exists, leaving it in place")
        else:
            os.makedirs(location)

    @staticmethod
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