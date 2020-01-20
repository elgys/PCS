This project simulates the forces on a gym wheel by a gymnast.

/exercises:
    All position files.
    Define all gym elements in terms of angles and forces.
        First argument is the angle of the wheel, when the action must be taken.
        Second argument is the function, which action must be taken.
        Further arguments are the arguments of the function.

human_model.py:
    This file contains all code associated with the modelling of a human body.
    It imports the physics.py file for all physics calculations.
    It reads humaninit.txt for the relative length of body parts for all calculations.

humaninit.txt:
    The relative length of body parts to the whole body.
    The first argument is the name of the body part.
    The second argument is the relative length.

physics.py:
     A collection of all physics calculations of the human model.

simulator.py:
     This file can read the .exc files and runs the whole simulation.
     It imports the wheel model and the human body model.

wheel_model.py:
    This file contains all code associated with the modelling of a gym wheel.
    It imports the human_model.py file for interactions with the human in the simulation.

For running this project you need at least python version 3.6 and the libraries
numpy, matplotlib and pymunk.
You can get the ....png by running main.py.
This runs the simulation, gets the data and than plots this.
