import numpy as np
import math
def getCenterOfMass(centerofmass,weight):
    """ This function takes the center of mass of multipule points in a 2D
        space and caculates a combined center of mass of the objects. It gets
        its input as [[x_cordinate1,y_cordinate1],[x_cordinate2,y_cordinate2]],
        [weight1,weight2]. And outputs [x_cordinate, y_cordinate]."""


    return np.average(centerofmass,axis=0,weights=weight)


def rotation2d(alpha):
    """ This function creates a rotation matrix."""

    return np.array([[np.cos(alpha),- np.sin(alpha)],[np.sin(alpha),np.cos(alpha)]])
