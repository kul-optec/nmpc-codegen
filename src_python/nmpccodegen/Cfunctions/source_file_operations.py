import os
from pathlib import Path
import time

class Source_file_generator:
    """
    Library to easily generate proximal functions
    """
    number_of_spaces_in_tab=4
    def __init__(self,location,function_type):
        """
        Parameters
        ---------
        location : target location 
        function_type : should be either "g" or "proxg"
        """
        self._location=location
        self._function_type=function_type
    def open(self):
        """
        Open fil stream
        """
        file = Path(self._location)
        if (file.exists()):
            print(self._location + " already exists, removing it before adding the new file")

        self._source_file = open(self._location, 'w')
        self._source_file.write("/* file generated on " + time.strftime("%x") +
                          " at " + time.strftime("%H:%M:%S") + " */" + "\n\n")

        if (self._function_type == "g"):
            print("generating g-type function")
            self._source_file.write("real_t casadi_interface_g(const real_t* state){\n")
        elif (self._function_type == "proxg"):
            print("generating proxg-type function")
            self._source_file.write("void casadi_interface_proxg(real_t* state){\n")
        else:
            print("ERROR wrong function_type pick either g or proxg")
            self._source_file.close()
    def start_for(self,iterator_name,length,indent):
        self.write_line("size_t "+iterator_name+ ";",indent)
        self.write_line("for("+iterator_name+"=0;i<"+str(length)+";i++){",indent)
    def close_for(self,indent):
        self.write_line("}",indent)
    def write_line(self,line,indent):
        string_indent = " "*indent*Source_file_generator.number_of_spaces_in_tab
        self._source_file.write(string_indent+line+"\n")
    def write_define(self,name,value,indent):
        self.write_line("#define "+name+" "+str(value),indent)
    def write_comment_line(self,line,indent):
        self.write_line("/* "+line+" */",indent)
    def set_output(self,output_index,value,indent):
        self.write_line("state["+str(output_index)+"]="+str(value)+";",indent)
    def close(self):
        self._source_file.write("\n}\n")

        self._source_file.close()