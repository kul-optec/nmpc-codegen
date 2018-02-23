import time

class Globals_generator:
    def __init__(self,location_globals):
        self._location_globals=location_globals
    def generate_globals(self,nmpc_controller):
        """ generate globals header file at location defined by constructor """
        print("Generating globals file at: "+self._location_globals)
        self._init_globals_file()

        self._generate_title("Problem specific definitions")
        self._define_variable("DIMENSION_INPUT", nmpc_controller.model.number_of_inputs)
        self._define_variable("DIMENSION_STATE", nmpc_controller.model.number_of_states)
        self._define_variable("DIMENSION_PANOC", nmpc_controller.dimension_panoc)
        self._define_variable("MPC_HORIZON", nmpc_controller.horizon)

        self._define_variable("NUMBER_OF_OBSTACLES", nmpc_controller.number_of_obstacles)
        self._define_variable("DEFAULT_OBSTACLE_WEIGHT", 1)

        self.set_data_type(nmpc_controller.data_type)

        self._generate_title("lbgfs solver definitions")
        self._define_variable("LBGFS_BUFFER_SIZE",nmpc_controller.lbgfs_buffer_size)

        self._generate_title("NMPC-PANOC solver definitions")
        self._define_variable("PANOC_MAX_STEPS",nmpc_controller.panoc_max_steps)
        self._define_variable("PANOC_MIN_STEPS",nmpc_controller.panoc_min_steps)
        self._define_variable("MIN_RESIDUAL","(1e"+str(nmpc_controller.min_residual)+")")

        self._generate_title("options used to test:")
        if(nmpc_controller.pure_prox_gradient):
            self._define_variable("PURE_PROX_GRADIENT", 1)

        self._generate_title("Optional features")
        if( nmpc_controller.integrator_casadi):
            self._define_variable("INTEGRATOR_CASADI","1")


    def _init_globals_file(self):
        """ internal function called at the start of the file generation """
        # replace globals file of it doesnt exist
        globals_file = open(self._location_globals, 'w')

        # print out the date and time to avoid confusion
        globals_file.write("/* file generated on " + time.strftime("%x") +
                           " at " + time.strftime("%H:%M:%S") + " */" + "\n\n")

        globals_file.close()
    def _define_variable(self,variable_name,variable_value):
        """ internal function generate a preprocessor variable """
        globals_file = open(self._location_globals, 'a')

        lines = ["#define ",variable_name ," ",str(variable_value),"\n"]
        globals_file.writelines(lines)

        globals_file.close()
    def generate_comment(self,comment):
        """ internal function generate single comment line """
        globals_file = open(self._location_globals, 'a')

        globals_file.write("/* "+comment+" */ \n")

        globals_file.close()
    def _generate_title(self,title):
        """ internal function used to generate titles in comments """
        globals_file = open(self._location_globals, 'a')

        globals_file.write("/*"+"\n" + "* ---------------------------------"+"\n")
        globals_file.write("* "+ title + "\n")
        globals_file.write("* ---------------------------------" + "\n"+"*/"+"\n")

        globals_file.close()
    def set_data_type(self,data_type):
        """ set the datatype to either "single precision" or "double precision" """
        if(data_type=="single precision"):
            self._generate_title("constants used with float data type")
            self._define_variable("real_t","float")
            self.generate_comment("data types have different absolute value functions")
            self._define_variable("ABS(x)", "fabsf(x)")
            self.generate_comment("Machine accuracy of IEEE float")
            self._define_variable("MACHINE_ACCURACY", "FLT_EPSILON")
            self.generate_comment("large number use with things like indicator functions")
            self._define_variable("LARGE", "100000")
        elif(data_type=="double precision"):
            self._generate_title("constants used with double data type")
            self._define_variable("real_t", "double")
            self.generate_comment("data types have different absolute value functions")
            self._define_variable("ABS(x)", "fabs(x)")
            self.generate_comment("Machine accuracy of IEEE double")
            self._define_variable("MACHINE_ACCURACY", "DBL_EPSILON")
            self.generate_comment("large number use with things like indicator functions")
            self._define_variable("LARGE", "10000000000")
        else:
            print("Error: invalid data type, not supported by globals generator")