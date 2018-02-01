import casadi as cd
import os
from pathlib import Path

class Casadi_code_generator:
    @ staticmethod
    def setup_casadi_functions_and_generate_c(initial_state,input_all_steps,
                                                state_reference,input_reference,
                                                obstacle_weights,cost,location_lib):

        cost_function = cd.Function('cost_function', [initial_state, input_all_steps,state_reference,input_reference,obstacle_weights], [cost])
        cost_function_derivative_combined = cd.Function('cost_function_derivative_combined',
                                                        [initial_state, input_all_steps,state_reference,input_reference,obstacle_weights],
                                                        [cost, cd.gradient(cost, input_all_steps)])

        Casadi_code_generator.translate_casadi_to_c(cost_function,location_lib, filename="cost_function.c")
        Casadi_code_generator.translate_casadi_to_c(cost_function_derivative_combined,location_lib, filename="cost_function_derivative_combined.c")

        return (cost_function,cost_function_derivative_combined)
    @ staticmethod
    def translate_casadi_to_c(casadi_function,location_lib,filename):
        # check if the buffer file excists, should never be the case, but check anyway
        buffer_file_name="buffer"
        file = Path(buffer_file_name)
        if (file.exists()):
            os.remove(buffer_file_name)

        # generate the casadi function in C to a buffer file
        opts = dict(verbose=False,
                    mex=False,
                    cpp=False,
                    main=False, 
                    # casadi_real="double",
                    codegen_scalars=False, 
                    with_header=False,                
                    with_mem=False,
                    # with_export=False
                    )
        casadi_function.generate(buffer_file_name,opts)
        file_name_costfunction = location_lib + "casadi/"+filename

        # check if the file already exists
        file = Path(file_name_costfunction)
        if(file.exists()):
            print(file_name_costfunction+ " already exists: removing file...")
            os.remove(file_name_costfunction)

        # move the function to the right location
        open(file_name_costfunction, 'a').close()

        prototype_function = "(const real_t** arg, real_t** res, int* iw, real_t* w, int mem) {"
        Casadi_code_generator.copy_over_function_to_file("buffer.c",file_name_costfunction,prototype_function)

        prototype_function = "(int *sz_arg, int* sz_res, int *sz_iw, int *sz_w) {"
        Casadi_code_generator.copy_over_function_to_file("buffer.c", file_name_costfunction, prototype_function)

        os.remove("buffer.c")

    @ staticmethod
    def copy_over_function_to_file(source,destination,function_name):
        in_file=False
        destination_file = open(destination, 'a')
        with open(source, 'r') as inF:
            for line in inF:
                if function_name in line:
                    in_file=True
                if in_file:
                    destination_file.write(line)
                if "}" in line:
                    in_file = False