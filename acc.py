import os
import numpy as np
import unsiotools.simulations.cfalcon as falcon
from potentials import *
from configparser import ConfigParser

# Usual Unit System: 
# [L] = kpc 
# [V] = km/s
# [M] = 1e10 Msun
# [T] = 0.98 Gyr
# [G] = 43007.1 kpc . (km/s)^2 . (1e10 Msun)^{-1}

filesList = os.listdir("./")
paramsfile = list(filter(lambda x: x.endswith(".ini"), filesList))[0]

config = ConfigParser()
config.read(paramsfile)

eps = config.getfloat('simulation', 'eps')   # softening length in case needed
G = config.getfloat('simulation', 'G')   
theta = config.getfloat('simulation', 'theta')

# Miyamoto-Nagai disk info
Md = config.getfloat('Miyamoto-Nagai', 'Md')
A = config.getfloat('Miyamoto-Nagai', 'A')
B = config.getfloat('Miyamoto-Nagai', 'B')

# Hernquist halo info
Mh = config.getfloat('Hernquist', 'Mh')
a = config.getfloat('Hernquist', 'a')


def newExtAcc(Data):
    PosVectors = Data[0]
    
    # Analytical potentials: functions defined at potentials.py
    # you can add new lines here in order to add new external potentials,
    # just keep in mind that the actual acceleration = - grad(potential)
    DiskAcc = - CartesianGradMNPotential(Md, A, B, PosVectors[:,0], PosVectors[:,1], PosVectors[:,2]) 
    HaloAcc = - CartesianGradHernquistPotential(Mh, a, PosVectors[:,0], PosVectors[:,1], PosVectors[:,2])
    
    # Add new accelations' arrays here
    AccVectors = np.array(DiskAcc + HaloAcc)
    
    return AccVectors     


def newFalconAcc(Data): 
    PosVectors = Data[0]
    Masses = Data[2]
    cf = Data[3]
    
    # Self gravity: uses UNSIOTOOLS getGravity method -- falcON algorithm
    ok, GravAcc, phi = cf.getGravity(PosVectors.flatten(), Masses, eps, G, theta=theta)
    GravAcc.shape = (int(len(GravAcc)/3), 3)
    
    return GravAcc

def newBothAcc(Data): 
    PosVectors = Data[0]
    Masses = Data[2]
    cf = Data[3]
    
    # Analytical potentials: functions defined at potentials.py
    # you can add new lines here in order to add new external potentials,
    # just keep in mind that the actual acceleration = - grad(potential)
    DiskAcc = - CartesianGradMNPotential(Md, A, B, PosVectors[:,0], PosVectors[:,1], PosVectors[:,2]) 
    HaloAcc = - CartesianGradHernquistPotential(Mh, a, PosVectors[:,0], PosVectors[:,1], PosVectors[:,2]) 
    
    # Self gravity: uses UNSIOTOOLS getGravity method -- falcON algorithm
    ok, GravAcc, phi = cf.getGravity(PosVectors.flatten(), Masses, eps, G, theta=theta)
    GravAcc.shape = (int(len(GravAcc)/3), 3)
    
    # Add new accelations' arrays here
    AccVectors = np.array(DiskAcc + HaloAcc + GravAcc)
    
    return AccVectors


