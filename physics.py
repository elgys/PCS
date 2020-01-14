# A file that collects physics caclulations we need to make it easier to reuse them.

import numpy as np
import math
def getCenterOfMass(centerofmass,weight):
    """
    This function will take center of masses of multipule points in a  2D
    space and caculate a center of mass of the objects togheter. This means it
    be done in  the way stated in input. we use this data first to caclulate
    total mass off a object. then it uses tose to calculate the impporance of every
    point in the list this will be use to cale to a list of vectors we can sumatt
    together to find the center of mass of multipule objects
    this is like averging all the vectors by wieght. this should be ablle to be used
    on general problems. or other way to look at this is a weigthed average.

    inputs
    centerofmass:[[x_cordinate1,y_cordinate1],[x_cordinate2,y_cordinate2]]
    weight: [weight1,weight2]

    output [x_cordinate, y_cordinate]
    """

    return np.average(centerofmass,axis=0,weights=weight)


def rotation2d(alpha):
    """
    This function creates a matrix to rotate.
    that made by  [[cos(alpha), -sin(alpha)],[sin(alpha),cos(alpha)]
    """

    return np.array([[np.cos(alpha),- np.sin(alpha)],[np.sin(alpha),np.cos(alpha)]])
