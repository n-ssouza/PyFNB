# PyFNB
PyFNB (Python + falcON + N-Body) is an implementation of [Jean-Charles Lambert's](https://gitlab.lam.fr/jclamber) python wrapper of UNSIOTOOLS into a simple N-Body simulation code. 
Hence, it uses [Walter Dehnen's](https://zah.uni-heidelberg.de/service/personnel?tx_zahinfothek_staff%5Baction%5D=show&tx_zahinfothek_staff%5Buid%5D=658&cHash=277cfe5c25b7f290fa28555202c8aa8f) very fast falcON algorithm in order to compute gravitational accelerations.

The code uses the leapfrog integration method, constant time step and it also allows for the addition of external analytical potentials.
The available output formats are: txt, GADGET-2 binary, HDF5. For the latter two, [Elvis Mello's](https://github.com/elvismello) version of [Rafael Ruggiero's](https://github.com/ruggiero) [``snapwrite.py``](https://github.com/elvismello/clustep/blob/master/clustep/snapwrite.py) from [clustep](https://github.com/elvismello/clustep) and [galstep](https://github.com/elvismello/galstep) is necessary. 

This piece of software may be useful for those who want to run quick average to (why not) high resolution N-Body simulations which involve only the calculations of gravitational forces and, at the same time, don't want to bother using GADGET or some other more complex code for this type of simulation.
Furthermore, this code's general structure is very instructive and educational for those who want to start exploring the world of numerical simulations.

# Required libraries
- os
- sys
- h5py
- struct
- numpy
- configparser
- [python-unsiotools](https://pypi.org/project/python-unsiotools/)

# Parameters file
The file `params.ini` contains the parameters regarding both the simulation itself and the external analytical potentials.
This is where you set the path to the initial conditions file, the output directory, activate self and/or external gravity, and so on.
Make sure you edited this file according to your desire before you run a simulation.

In case external gravity is not activated, the parameters of the external potentials are useless, however there's no need no comment those lines. The same is true for self gravity, if it's not activated there's no need to comment the softening length parameter, for example.
Notice that it doesn't make sense for both self and external gravities to be deactivated, if this happens the program raises an error and then it halts.

**Important notes:** 
  - There should be only one parameter file within the directory where ``PyFNB.py`` is located
  - The name of the parameters file can be anything as long as it ends with `.ini`

# Initial Conditions
For the moment, the code only accepts initial conditions files following the scheme:

- It has to be a txt file
- If self gravity is activated, then it has to contain 7 columns of data: `x, y, z, vx, vy, vz, masses`
- If self gravity is not activated, then it has to contain 6 columns of data: `x, y, z, vx, vy, vz`

For more clarity, see the example initial conditions file.

# Usage
Edit the parameters file `params.ini` as you want and then run the main script

```
python3 PyFNB.py
```
In case the specified output directory doesn't exist, it will be created.

# Adding new external analytical potentials
For now, the code only supports time independent external potentials. Those can be added this way: 
  1. You need to write a new function at ``potentials.py`` which will return an (N,3) array, where N is the number of particles, containing each particle's acceleration vector due to this new field. Keep in mind that accelation is equivalent to minus the gradient of the potential. 
  2. Then you need to call this new function at ``acc.py`` and add these new accelerations into ``AccVectors``, as it is done for the already available potentials.

# Examples
This video was made from the outputs of a simulation where self gravity was deactivated. The initial conditions file used here is ``examples/ics/plummerForOnlyExtgrav.txt``

https://user-images.githubusercontent.com/73209038/156273282-43f6d4fe-6a5f-43fa-91d7-83740fc07c22.mp4

This other video represents the same scenario of the last one, but with self gravity activated. The initial conditions file used here is ``examples/ics/plummerForBoth.txt``

https://user-images.githubusercontent.com/73209038/156273526-b0cb8d98-9678-4409-9e6e-58430d115836.mp4

For both examples, the parameters of the external analytical potentials are the same ones as in ``params.ini`` uploaded here.
