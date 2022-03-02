import os
import numpy as np
from configparser import ConfigParser

'''
Here we have the definitions of the available external analytical potentials.
What is actually used are they Gradient functions, because in practice acceleration = - grad(potential)
Feel free to add another functions as well as the new respective parameters into params.ini
'''


# Gravitational constant is set from parameters file

filesList = os.listdir("./")
paramsfile = list(filter(lambda x: x.endswith(".ini"), filesList))[0]

config = ConfigParser()
config.read(paramsfile)
G = config.getfloat('simulation', 'G') 


def MNPotentialCartesian(Md, A, B, x, y, z):
    return - (G * Md) / (np.sqrt(np.square(x) + np.square(y) + np.square(np.sqrt(np.square(z) + np.square(B)) + A)))


def MNPotentialCylindrical(Mh, A, B, R, z):
    return - (G * Mh) / (np.sqrt(np.square(R) + np.square(np.sqrt(np.square(z) + np.square(B)) + A)))


def CartesianGradMNPotential(Md, A, B, x, y, z):
    Fx = G * Md * x * np.power((np.square(x) + np.square(y) + np.square(np.sqrt(np.square(z) + np.square(B)) + A)), -1.5)
    Fy = G * Md * y * np.power((np.square(x) + np.square(y) + np.square(np.sqrt(np.square(z) + np.square(B)) + A)), -1.5)
    Fz = G * Md * z * np.power((np.square(x) + np.square(y) + np.square(np.sqrt(np.square(z) + np.square(B)) + A)), -1.5) * (1 + (A * np.power((np.square(z) + np.square(B)), -0.5)))
    
    ForceVector = np.column_stack((Fx, Fy, Fz))
    
    return ForceVector 


def HernquistPotentialCartesian(Mh, a, x, y, z):
    return - (G * Mh) / (np.sqrt(np.square(x) + np.square(y) + np.square(z)) + a)         


def HernquistPotentialSpherical(Mh, a, r):
    return - (G * Mh) / (r + a)


def CartesianGradHernquistPotential(Mh, a, x, y, z):
    Fx = G * Mh * x * np.power((np.sqrt(np.square(x) + np.square(y) + np.square(z)) + a), -2) * np.power((np.square(x) + np.square(y) + np.square(z)), -0.5)        
    Fy = G * Mh * y * np.power((np.sqrt(np.square(x) + np.square(y) + np.square(z)) + a), -2) * np.power((np.square(x) + np.square(y) + np.square(z)), -0.5)       
    Fz = G * Mh * z * np.power((np.sqrt(np.square(x) + np.square(y) + np.square(z)) + a), -2) * np.power((np.square(x) + np.square(y) + np.square(z)), -0.5)       

    ForceVector = np.column_stack((Fx, Fy, Fz))

    return ForceVector

