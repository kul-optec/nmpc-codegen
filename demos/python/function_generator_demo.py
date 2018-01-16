import sys
sys.path.insert(0, '../../src_python')
import nmpccodegen.Cfunctions as cfunctions

test = cfunctions.IndicatorBoxFunction([1,2],[3,4])
test.generate_c_code("test.c")
test.prox.generate_c_code("test_prox.c")