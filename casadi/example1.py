# This is a small demo of casdi, generating a function with its jacobian
from casadi import *

x = MX.sym('x ',2) 
y = MX.sym('y') 
f = Function('f',[x ,y],[x,sin(y)*x],['x','y'],['r','q'])
fd=f.jacobian('x')

f.generate('gen_f.c')

# print out the 2 functions
# print(f)
print(fd)

# print(f([1,1],5))
# print(fd([1,1],5))

