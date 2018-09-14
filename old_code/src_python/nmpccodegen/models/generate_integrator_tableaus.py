# this file is Linux/mac only as it uses the nodepy lib, 
# the results are saved in text files that are in the repo. 
# So no need for non developers to ever touch this.

import nodepy as nodepy
import numpy as np
from nodepy.runge_kutta_method import *
import tabulate as t
import scipy.io as spio

def save_integrator(key_name):
    """ 
    save the integrator if its explicit 

    Parameters
    ---------
    key_name
    """
    RK=loadRKM(key_name)
    if(RK.is_explicit()):
        print("Saving "+RK.name+" to file "+str(key_name)+".npz" + " and file "+str(key_name)+".mat")

        # an integrator tablaeu exists out of 3 matrices:
        #A=np.asarray(RK.A)
        #b=np.asarray(RK.b)
        #c=np.asarray(RK.c)
	
        A=np.array(RK.A.tolist()).astype(np.float64)
        b=np.array(RK.b.tolist()).astype(np.float64)
        c=np.array(RK.c.tolist()).astype(np.float64)

        output_file="./integrator_tableaus/"+str(key_name)

        # save into python matrix file
        np.savez(output_file, A=A, b=b, c=c)

        output_file="../../../src_matlab/+nmpccodegen/+models/integrator_tableaus/"+str(key_name)

        # save into matlab matrix file
        spio.savemat( output_file, dict([('A', A), ('b', b), ('c', c)]) )

        return True
    return False

def generate_manual_page(keys_explicit_integrators):
    """
    Generates latex table with key names
    """
    tex_tile = open('table_integrators.tex', 'w')
    names_explicit_integrators=[]
    for i in range(0,len(keys_explicit_integrators)):
        RK=loadRKM(keys_explicit_integrators[i])
        names_explicit_integrators.append(RK.name)

    headers=["key","integrator_name"]
    table=[keys_explicit_integrators,names_explicit_integrators]
    tex_tile.write(t.tabulate(zip(*table), headers, tablefmt="latex"))
    tex_tile.close()
    
def main():
    RK=loadRKM()
    keys_integrators = sorted(RK.keys())
    number_of_integrators=len(keys_integrators)
    # print(keys_integrators)
    print("Start generating available integrator schemes")

    explicit_integrators=[]
    for i in range(0,number_of_integrators):
        if(save_integrator(keys_integrators[i])):
            explicit_integrators.append(keys_integrators[i])

    number_of_explicit_integrators=len(explicit_integrators)
    print(str(number_of_explicit_integrators)+" explicit integrators found")

    # generate a simple overview of these integrators
    generate_manual_page(explicit_integrators)


if __name__ == '__main__':
    main()
