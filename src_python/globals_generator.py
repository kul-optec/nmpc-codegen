import time


class Globals_generator:
    def __init__(self,location_globals):
        self._location_globals=location_globals
    def generate_globals(self,nmpc_controller):
        print("Generating globals file at: "+self._location_globals)
        self.init_globals_file()

        self.generate_title("Problem specific definitions")
        self.define_variable("DIMENSION_INPUT", nmpc_controller.model.number_of_inputs)
        self.define_variable("DIMENSION_STATE", nmpc_controller.model.number_of_states)
        self.define_variable("MPC_HORIZON", nmpc_controller.number_of_steps)

        self.set_data_type(nmpc_controller.data_type)

        self.generate_title("lbgfs solver definitions")
        self.define_variable("LBGFS_BUFFER_SIZE",nmpc_controller.lbgfs_buffer_size)

        self.generate_title("NMPC-PANOC solver definitions")
        self.define_variable("PANOC_MAX_STEPS",nmpc_controller.panoc_max_steps)

        self.generate_title("Optional features")
        if( nmpc_controller.integrator_casadi):
            self.define_variable("INTEGRATOR_CASADI","1")


    def init_globals_file(self):
        # replace globals file of it doesnt exist
        globals_file = open(self._location_globals, 'w')

        # print out the date and time to avoid confusion
        globals_file.write("/* file generated on " + time.strftime("%x") +
                           " at " + time.strftime("%H:%M:%S") + " */" + "\n\n")

        globals_file.close()
    def define_variable(self,variable_name,variable_value):
        globals_file = open(self._location_globals, 'a')

        lines = ["#define ",variable_name ," ",str(variable_value),"\n"]
        globals_file.writelines(lines)

        globals_file.close()
    def generate_comment(self,comment):
        globals_file = open(self._location_globals, 'a')

        globals_file.write("/* "+comment+" */ \n")

        globals_file.close()
    def generate_title(self,title):
        globals_file = open(self._location_globals, 'a')

        globals_file.write("/*"+"\n" + "* ---------------------------------"+"\n")
        globals_file.write("* "+ title + "\n")
        globals_file.write("* ---------------------------------" + "\n"+"*/"+"\n")

        globals_file.close()
    def set_data_type(self,data_type):
        if(data_type=="single precision"):
            self.generate_title("constants used with float data type")
            self.define_variable("real_t","float")
            self.generate_comment("data types have different absolute value functions")
            self.define_variable("ABS(x)", "fabsf(x)")
            self.generate_comment("Machine accuracy of IEEE float")
            self.define_variable("MACHINE_ACCURACY", "pow(10,-8)")
            self.generate_comment("large number use with things like indicator functions")
            self.define_variable("LARGE", "100000")
        elif(data_type=="double precision"):
            self.generate_title("constants used with double data type")
            self.define_variable("real_t", "double")
            self.generate_comment("data types have different absolute value functions")
            self.define_variable("ABS(x)", "fabs(x)")
            self.generate_comment("Machine accuracy of IEEE float")
            self.define_variable("MACHINE_ACCURACY", "pow(10,-16)")
            self.generate_comment("large number use with things like indicator functions")
            self.define_variable("LARGE", "10000000000")
        else:
            print("Error: invalid data type, not supported by globals generator")