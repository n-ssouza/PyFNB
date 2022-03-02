import os 
import numpy as np
from sys import exit
from configparser import ConfigParser
from snapwrite import write_snapshot
import acc

# Usual Unit System: 
# [L] = kpc 
# [V] = km/s
# [M] = 1e10 Msun
# [T] = 0.98 Gyr
# [G] = 43007.1 kpc . (km/s)^2 . (1e10 Msun)^{-1}



def main(): 
    init()
    
    Data = GetData()
   
    if (selfgrav):
        import unsiotools.simulations.cfalcon as falcon
        cf = falcon.CFalcon()
        Data.append(cf)
        if (externalgrav):
            NewAcc = acc.newBothAcc
        else:
            NewAcc = acc.newFalconAcc

    else:
        NewAcc = acc.newExtAcc


    if not (out_format == 'txt' or out_format == 'gadget2' or out_format == 'hdf5'):
        exit("Invalid file format")
    else:
        if (out_format == 'txt'):
            write_output = write_txt
        else:
            write_output = snapwrite 
        

    OldAcc = NewAcc(Data)
    
    # Loop over time: Leapfrog integration
    t = tstart
    filenumber = 0
    step = 0
    while(t < tstop):
    
        # Current time:
        t = tstart + step*dt
    
        # Updating positions:
        Data[0] = NewPos(Data[0], Data[1], OldAcc, dt)
    
        # Updating accelerations:
        CurrAcc = NewAcc(Data)
 
        # Updating velocities:
        Data[1] = NewVel(Data[1], OldAcc, CurrAcc, dt)
    
        # Setting old accelerations as the current ones:
        OldAcc = CurrAcc

        # Saving data:                                                       
        if (step % n == 0):
            write_output(Data, filenumber)
            
            filenumber = filenumber + 1
            
        step = step + 1


def init(): 
    global tstart, tstop, dt, n, ic_dir, out_dir, out_format, selfgrav, externalgrav

    filesList = os.listdir("./")
    paramsfile = list(filter(lambda x: x.endswith(".ini"), filesList))[0]
    
    config = ConfigParser()
    config.read(paramsfile)

    ic_dir = config.get('simulation', 'ic_dir')
    out_dir = config.get('simulation', 'out_dir')
    out_format = config.get('simulation', 'out_format')
    tstart = config.getfloat('simulation', 'tstart')
    tstop = config.getfloat('simulation', 'tstop')
    dt = config.getfloat('simulation', 'dt')
    n = config.getint('simulation', 'n')    # 1 file every n steps
    selfgrav = bool(config.getint('simulation', 'selfgrav'))
    externalgrav = bool(config.getint('simulation', 'externalgrav'))

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
   
def GetData():
    
    # if self gravity is activated, then GetData needs
    # to retrieve 7 columns of data: x, y, z, vx, vy, vz, masses
    
    # if only external gravity is activated, the GetData needs
    # to retrieve 6 columns of data: x, y, z, vx, vy, vz
  
    # if neither self nor external gravity are activated, then
    # the program halts

    # Reading initial conditions:

    if (os.path.exists(ic_dir)): 
        Data = np.loadtxt(ic_dir, dtype='float32')
        
        # get number of columns
        numCol = np.atleast_2d(Data).shape[1]
       
        if (selfgrav or externalgrav):

            if (selfgrav):  
                if (numCol == 7):
                    Data = np.split(Data, [3,6], axis=1)
                    Data[2] = Data[2].flatten()            
                    return Data
                else:
                    exit("Self gravity is activated, but initial conditions file doesn't have 7 columns of data\n")
            
            else:  # only external gravity is activated
                if (numCol == 6):
                    Data = np.split(Data, [3], axis=1) 
                    return Data 
                else:
                    exit("Only external gravity is activated, but initial conditions file doesn't have 6 columns of data\n")
        
        else:
            exit("Neither self nor external gravity were activated\n") 
    else:        
        exit("Invalid path to initial conditions file\n")


# Updates position vectors: leapfrog
def NewPos(currPos, currVel, currAcc, dt):
    return currPos + currVel*dt + 0.5*currAcc*(dt**2)


# Updates velocity vectors: leapfrog 
def NewVel(currVel, currAcc, newAcc, dt):
    return currVel + 0.5*(currAcc + newAcc)*dt


# write output on txt files
def write_txt(Data, filenumber):
     
    filename = "file{:0>4}.txt".format(filenumber)
    
    #Header info:
    info = "Output data from PyFNB.py"
    info += "     position_x           position_y           position_z           velocity_x           velocity_y           velocity_z"           
    
    if (selfgrav):
        info += "           masses"
        OutData = np.column_stack((Data[0], Data[1], Data[2]))
    else:
        OutData = np.column_stack((Data[0], Data[1]))
    
    np.savetxt(out_dir + filename, OutData, header = info, fmt = "%20.8e")

    print("{} DONE".format(filename))


# write output on gadget2 binary or hdf5 formats
def snapwrite(Data, filenumber):

    filename = "file{:0>4}".format(filenumber)

    PosVectors = np.array(Data[0], order='C')
    VelVectors = np.array(Data[1], order='C')
    Masses = Data[2]
    
    PosVectors.shape = (1, -1)
    VelVectors.shape = (1, -1)

    # Number of particles:
    N = len(Masses)

    # Number of particles of each gadget type:
    n_part = [0, N, 0, 0, 0, 0]  # only DM particles
                                 # what matters is that only
                                 # self gravity is considered
    
    IDs = np.arange(1, N + 1)
    
    data_list = [PosVectors[0], VelVectors[0], IDs, Masses]
    
    write_snapshot(n_part, data_list, outfile = out_dir + filename, file_format = out_format)

    print("{} DONE".format(filename))


if (__name__ == '__main__'):
    main()
