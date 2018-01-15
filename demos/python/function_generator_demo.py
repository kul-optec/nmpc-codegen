
import sys
sys.path.append('../../src_python')
import Cfunctions.IndicatorBoxFunction as indbox

test = indbox.IndicatorBoxFunction([1,2],[3,4])
test.generate_c_code("test.c")
test.prox.generate_c_code("test_prox.c")