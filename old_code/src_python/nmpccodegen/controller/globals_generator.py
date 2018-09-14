import time

class Globals_generator:
    def __init__(self,location_globals):
        """
        Constructs a Globals generator object

        Parameters
        ---------
        """
        self._location_globals=location_globals
    def generate_globals(self,nmpc_controller):
        """ 
        Generate globals header file at location defined by constructor 

        Parameters
        ---------
        nmpc_controller : object that represents controller
        """
        print("Generating globals file at: "+self._location_globals)
        self._init_globals_file()

        self._generate_title("Problem specific definitions")
        self._define_variable("DIMENSION_INPUT", nmpc_controller.model.number_of_inputs)
        self._define_variable("DIMENSION_STATE", nmpc_controller.model.number_of_states)
        self._define_variable("DIMENSION_PANOC", nmpc_controller.dimension_panoc)
        self._define_variable("MPC_HORIZON", nmpc_controller.horizon)
        if(nmpc_controller.shift_input):
            self._define_variable("SHIFT_INPUT", str(1.))

        self._generate_title("Lagrangian related values, only visible if there are general constraints")
        if(len(nmpc_controller.general_constraints)>0):
            self._define_variable('USE_LA', '1')
            self._define_variable('NUMBER_OF_GENERAL_CONSTRAINTS',
                                  str(len(nmpc_controller.general_constraints) * nmpc_controller.horizon))
            self._define_variable('NUMBER_OF_GENERAL_CONSTRAINTS_PER_STEP',
                                  str(len(nmpc_controller.general_constraints)))
            self._define_variable('CONSTRAINT_OPTIMAL_VALUE', str(nmpc_controller.constraint_optimal_value))
            self._define_variable('CONSTRAINT_MAX_WEIGHT', str(nmpc_controller.constraint_max_weight))
            self._define_variable('START_RESIDUAL', str(nmpc_controller.start_residual))
            self._define_variable('MAX_STEPS_LA', str(nmpc_controller.max_steps_LA))

        self._generate_title("Constraint related values")
        self._define_variable("NUMBER_OF_CONSTRAINTS", nmpc_controller.number_of_constraints)
        self._define_variable("DEFAULT_CONSTRAINT_WEIGHT", 1)

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
        """ 
        Internal function called at the start of the file generation 
        """
        # replace globals file of it doesnt exist
        globals_file = open(self._location_globals, 'w')

        # print out the date and time to avoid confusion
        globals_file.write("/* file generated on " + time.strftime("%x") +
                           " at " + time.strftime("%H:%M:%S") + " */" + "\n\n")

        globals_file.close()
    def _define_variable(self,variable_name,variable_value):
        """ 
        Internal function generate a preprocessor variable 

        Parameters
        ---------
        variable_name
        variable_value
        """
        globals_file = open(self._location_globals, 'a')

        lines = ["#define ",variable_name ," ",str(variable_value),"\n"]
        globals_file.writelines(lines)

        globals_file.close()
    def generate_comment(self,comment):
        """ 
        Internal function generate single comment line 

        Parameters
        ---------
        comment : string that contains comment line
        """
        globals_file = open(self._location_globals, 'a')

        globals_file.write("/* "+comment+" */ \n")

        globals_file.close()
    def _generate_title(self,title):
        """ 
        Internal function used to generate titles in comments 

        Parameters
        ---------
        title
        """
        globals_file = open(self._location_globals, 'a')

        globals_file.write("/*"+"\n" + "* ---------------------------------"+"\n")
        globals_file.write("* "+ title + "\n")
        globals_file.write("* ---------------------------------" + "\n"+"*/"+"\n")

        globals_file.close()
    def set_data_type(self,data_type):
        """ 
        Sets the datatype to either "single precision" or "double precision" 

        Parameters
        ---------
        data_type : precision of the solver is "single precision" or "double precision" 
        """
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