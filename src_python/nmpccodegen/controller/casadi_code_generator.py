import casadi as cd
import os
import sys
from pathlib import Path

class Casadi_code_generator:
    @ staticmethod
    def setup_casadi_functions_and_generate_c(static_casadi_parameters,input_all_steps,
                                                obstacle_weights,cost,location_lib):

        cost_function = cd.Function('cost_function', [static_casadi_parameters, input_all_steps,obstacle_weights], [cost])
        cost_function_derivative_combined = cd.Function('cost_function_derivative_combined',
                                                        [static_casadi_parameters, input_all_steps,obstacle_weights],
                                                        [cost, cd.gradient(cost, input_all_steps)])

        Casadi_code_generator.translate_casadi_to_c(cost_function,location_lib, filename="cost_function")
        Casadi_code_generator.translate_casadi_to_c(cost_function_derivative_combined,location_lib, filename="cost_function_derivative_combined")

        return (cost_function,cost_function_derivative_combined)

    @staticmethod
    def generate_c_constraints(initial_state, input_all_steps, constraint_values, location_lib):
        constraints_function = cd.Function("evaluate_constraints", [initial_state, input_all_steps],[constraint_values])
        Casadi_code_generator.translate_casadi_to_c(constraints_function, location_lib,filename="evaluate_constraints")

    @ staticmethod
    def translate_casadi_to_c(casadi_function,location_lib,filename):
        # check if the buffer file excists, should never be the case, but check anyway
        buffer_file_name="buffer"
        file = Path(buffer_file_name)
        if (file.exists()):
            os.remove(buffer_file_name)

        version_casadi = cd.CasadiMeta.version();
        version_split=version_casadi.split(".")

        major_version = version_split[0]
        minor_version = version_split[1]

        # generate the casadi function in C to a buffer file
        if(major_version=="3" and minor_version=="4"):
            opts = dict(verbose=False,
                        mex=False,
                        cpp=False,
                        main=False, 
                        # casadi_real="double",
                        codegen_scalars=False, 
                        with_header=True,                
                        with_mem=False,
                        with_export=False,
                        casadi_int="long int",
                        )
        elif(major_version=="3" and minor_version=="3"):
            opts = dict(verbose=False,
                        mex=False,
                        cpp=False,
                        main=False,
                        codegen_scalars=False, 
                        with_header=True,                
                        with_mem=False,
                        with_export=False
                        )
        elif(major_version=="3" and minor_version=="2"):
            opts = dict(verbose=False,
                        mex=False,
                        cpp=False,
                        main=False,
                        codegen_scalars=False,
                        with_header=True,
                        with_mem=False,
                        )
        else:
            error_message =  "Error: unsupported version of Casadi"
            sys.exit(error_message)

        casadi_function.generate(filename,opts)
        file_name_costfunction = location_lib + "/casadi/"+filename

        # check if the files already exist
        file = Path(file_name_costfunction+".c")
        if(file.exists()):
            print(file_name_costfunction+".c"+ " already exists: removing file...")
            os.remove(file_name_costfunction+".c")
        file = Path(file_name_costfunction + ".h")
        if (file.exists()):
            print(file_name_costfunction + ".h" + " already exists: removing file...")
            os.remove(file_name_costfunction + ".h")

        os.rename(filename+".c", file_name_costfunction+".c")
        os.rename(filename+".h", file_name_costfunction+".h")