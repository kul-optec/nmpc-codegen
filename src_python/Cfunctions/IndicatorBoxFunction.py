import Cfunctions.ProximalFunction
import Cfunctions.Function
import Cfunctions.source_file_operations as sfo

class IndicatorBoxFunctionProx(Cfunctions.Function.Cfunction):
    def __init__(self,lower_limits,upper_limits):
        """constructor box function"""
        self._lower_limits=lower_limits
        self._upper_limits=upper_limits
        self._dimension=min(len(upper_limits),len(lower_limits))
        if(len(lower_limits)!=len(upper_limits)):
            print("Error limits length do not match, using the smallest of the two: dimension=" \
                  +str(self._dimension))

    def generate_c_code(self, location):
        source_file = sfo.Source_file_generator(location,"proxg")
        source_file.open()

        for dimension in range(0,self._dimension):
            source_file.write_comment_line(\
                "check if the value of the border is outside the box, if so go to the nearest point inside the box", \
                indent=1)
            source_file.write_line("if(input["+str(dimension)+"]<"+str(self._lower_limits[dimension])+"){",indent=1)
            source_file.set_output(dimension,str(self._lower_limits[dimension]),2)
            source_file.write_line("}else{",1)
            source_file.set_output(dimension, "input["+str(dimension)+"]", 2)
            source_file.write_line("}", 1)

            source_file.write_line("if(input[" + str(dimension) + "]>" + str(self._upper_limits[dimension]) + "){",
                                   indent=1)
            source_file.set_output(dimension, str(self._upper_limits[dimension]), 2)
            source_file.write_line("}else{", 1)
            source_file.set_output(dimension, "input[" + str(dimension) + "]", 2)
            source_file.write_line("}", 1)

        source_file.close()

class IndicatorBoxFunction(Cfunctions.ProximalFunction.ProximalFunction):
    def __init__(self,lower_limits,upper_limits):
        super().__init__(IndicatorBoxFunctionProx(lower_limits, upper_limits))
        """constructor box function"""
        self._lower_limits=lower_limits
        self._upper_limits=upper_limits
        self._dimension=min(len(upper_limits),len(lower_limits))
        if(len(lower_limits)!=len(upper_limits)):
            print("Error limits length do not match, using the smallest of the two: dimension=" \
                  +str(self._dimension))

    def generate_c_code(self, location):
        source_file = sfo.Source_file_generator(location,"g")
        source_file.open()

        for dimension in range(0,self._dimension):
            source_file.write_comment_line("check if the value of the border is outside the box, if so return zero", \
                                           indent=1)
            source_file.write_line("if(input["+str(dimension)+"]<"+str(self._lower_limits[dimension])+ \
                              " || input["+str(dimension)+"]>"+str(self._upper_limits[dimension])+ \
                              "){",indent=1)
            source_file.write_line("return LARGE;", indent=2)
            source_file.write_line("}",indent=1)

        source_file.write_comment_line("if the value's where never outside the box, return zero",indent=1)
        source_file.write_line("return 0;", indent=1)
        source_file.close()

def main():
    test = IndicatorBoxFunction([1,2],[3,4])
    test.generate_c_code("test.c")

if __name__ == "__main__":
    main()