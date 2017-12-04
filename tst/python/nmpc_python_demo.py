# little hack to import the local lib and not work with the one in the path
import sys
sys.path.insert(0, '../../src_python')

import ctypes
import simulator

# simulation_cleanup
def main():
    current_state = [ 0.2, 0. , 0.4,0. , 0.6 , 0. , 0.8 , 0. \
                    ,1. , 0., \
                    0.,0., 0.,0.,0.,0.,0.,0. ]

    sim = simulator.Simulator('../../')
    (test,optimal_input) = sim.simulate_nmpc(current_state,2)

    print(str(optimal_input[0])+"<->"+str(test))


if __name__ == "__main__":
    main()