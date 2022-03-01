# PyFNB
PyFNB (Python + Falcon + N-Body) is an implementation of Jean-Charles Lambert's python wrapper of UNSIOTOOLS into a simple N-Body simulation code. 
Hence, it uses Walter Dehnen's very fast falcON algorithm in order to compute gravitational accelerations. 
The code uses the leapfrog integration method, constant time step and it also allows for the addition of external analytical potentials.

# Required libraries
- sys
- os
- numpy
- configparser
- [python-unsiotools](https://pypi.org/project/python-unsiotools/)

# Parameters file
The file `params.ini` contains the parameters regarding both the simulation itself and the external analytical potentials.
This is where you set the path to the initial conditions file, the output directory, activate self and/or external gravity, and so on.
Make sure you edited this file according to your desire before you run a simulation.
In case external gravity is not activated, the parameters of the external potentials are useless, however there's no need no comment those lines. The same is true for self gravity, if it's not activated there's no need to comment the softening length parameter, for example.
Notice that it doesn't make sense for both self and external gravities to be deactivated, if this happens the program raises an error and then it halts.

Important note: the name of the parameters file can be anything as long as it ends with `.ini`

# Initial Conditions
For the moment, the code only accepts initial conditions' files following the scheme:

- It has to be a txt file
- If self gravity is activated, then it has to contain 7 columns of data: `x, y, z, vx, vy, vz, masses`
- If self gravity is not activated, then it has to contain 6 columns of data: `x, y, z, vx, vy, vz`

# Usage
Edit the parameters file `params.ini` as you want and then run the main script

```
python3 PyFNB.py
```

# Adding new external analytical potentials
For now, the code only supports time independent external potentials. Those can be added this way: 
  1. you need to write a new function at ``potentials.py`` which will return an array containing each particle's acceleration due to this new field. Keep in mind that accelation equal minus the gradient of the potential. 
  2. Then you need to call this new function at ``acc.py`` and add these new accelerations into ``AccVectors``. The default shape of the array containing all the acceleration vectors is (N,3), where N is the number of particles.





