from casadi import *
from os import *
from sys import *

x = MX.sym('x ',2) 
f = Function('f',[x],[sin(x)],['x'],['r'])

# Generate the c file with 
f.generate('buffer.c')

# move the c file because apparently casadi crashes with a path for no reason
os.rename('buffer.c',sys.argv[1])

print('GENERATING f.c for a simple test')