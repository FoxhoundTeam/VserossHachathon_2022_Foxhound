import ctypes
import os
 
libObject = ctypes.CDLL('C:\dllExample\QuadrotorModel.dll')

X = (ctypes.c_double * 10)()
Z = (ctypes.c_double * 10)()

#cppfunc(100, 0, 32, 50, xArr, zArr, 7, 100, 0, -5, -2);
for i in range(10):
    X[i] = i*10
    Z[i] = i*10

states = libObject.cppfunc(0, 0, 32, 50, X, Z, 10, 30, 30, 0, 0)

print(states)