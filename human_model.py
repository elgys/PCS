import numpy as np
import physics as p

class human:

    dic = {}
    def  __init__(self,length,weight,bodyposition,shouldersize):
        # here the values are given in degrees.
        self.head = 0
        self.torso = 0
        self.rightUpperArm = 0
        self.rightLowerArm = 0
        self.rightUpperLeg = 0
        self.rightLowerLeg = 0
        self.leftUpperArm = 0
        self.leftLowerArm = 0
        self.leftUpperLeg = 0
        self.leftLowerLeg = 0
        # length in cm
        self.length = length
        # weigth in kilo
        self.weight = weight
        # the bodyposition is the position of the middle of the body
        self.bodyposition = np.array(bodyposition)
        # the midsize of a shoulder
        self.shoulderSize = shouldersize
        # gymnast not turned
        self.turned = False

        if "done" not in self.dic.keys():
            self.dic["done"] = 1
            f = open("humaninit.txt",'r')

            for line in f:
                (key,value) = line.split()
                self.dic[key] = float(value)

        self.cog = self.__getCenterOfMass()

    def __rotationBodyParts(self,begin,end,rot):
        """ Rotate a bodypart whithout knowing which bodypart it is, by
            using a vector describing the bodypart.
            It returns (vector, end coordinate)"""
        vec = end - begin
        vec = np.dot(p.rotation2d(rot),vec)
        end = begin + vec

        return(vec,end)

    def __legcalc(self,topposition,legrot,Upper=True):
        """ Calculate of the upper or lower leg its end coordinate (knee or
            foot), rotate it and calculate its center of mass and its mass.
            Returns (center of mass, weight, end coordinate)."""
        if Upper:
            string = "_Upper_Leg"
        else:
            string = "_Lower_Leg"

        lowerPart = topposition - np.array([0,self.dic["length"+string] * self.length])
        (vec,lowerPart) = self.__rotationBodyParts(topposition,lowerPart,legrot)
        cog = topposition + vec * self.dic["cog"+ string]
        mass = self.weight * self.dic["weight"+ string]

        return (cog,mass,lowerPart)

    def __armcalc(self,topposition,armrot,Upper=True,right = True):
        """ Calculate of the upper or lower arm its end coordinate (elbow or
            hand), rotate it and calculate its center of mass and its mass.
            Returns (center of mass, weight, end coordinate)."""
        if Upper:
            string = "_Upper_Arm"
        else:
            string = "_Lower_Arm"

        if right:
            lowerPart = topposition - np.array([self.dic["length"+string] * self.length,0])
        else:
            lowerPart = topposition + np.array([self.dic["length"+string] * self.length,0])

        (vec,lowerPart) = self.__rotationBodyParts(topposition,lowerPart,armrot)
        cog = lowerPart + vec *(1- self.dic["cog"+ string])
        mass = self.weight * self.dic["weight"+ string]

        return (cog,mass,lowerPart)

    def __headcalc(self,neck,headrot):
        """ Calculate of the head its end coordinate (top of a head),
            rotates it and calculate its center of mass and its mass.
            Returns (center of mass, weight, end coordinate)."""
        tophead = neck + np.array([0,self.length * self.dic["length_Head"]])
        (vec,tophead) = self.__rotationBodyParts(neck,tophead,self.head)
        cog = neck + vec * (1 - self.dic["cog_Head"])
        mass = self.weight * self.dic["weight_Head"]

        return(cog,mass,tophead)

    def __getCenterOfMass(self):
        """ Calculate the center of mass of the total body.
            Returns ([individual center of masses], [individual weights]).
            we also caclulate the location of the other parts and put them in
            ourself."""
        CenterofMass=[]
        masses = []
        # Calculate the placement of the legs and their combined center of mass.
        legMiddle = self.bodyposition - (np.array([0,self.length * self.dic["length_Body"] /2]))
        (vec,legMiddle)= self.__rotationBodyParts(self.bodyposition,legMiddle,self.torso)

        if self.turned:
            sideLength = [0,0]
        else:
            sideLength = [self.shoulderSize/ 2,0]

        rightLeg = legMiddle - sideLength
        leftLeg = legMiddle + sideLength
        self.locationRightHip = rightLeg
        self.locationLeftHip = leftLeg
        # left upper leg caclulations
        (cogLeftUpperLeg,mass,leftKnee)= self.__legcalc(leftLeg,self.leftUpperLeg)
        self.locationLeftKnee = leftKnee
        CenterofMass.append(cogLeftUpperLeg)
        masses.append(mass)
        # left lower leg caclulations
        (cogLeftLowerLeg,mass,leftFoot) = self.__legcalc(leftKnee,self.leftLowerLeg,False)
        self.locationLeftFoot = leftFoot
        CenterofMass.append(cogLeftLowerLeg)
        masses.append(mass)
        # right upper leg caclulations
        (cogRightUpperLeg,mass,rightKnee)= self.__legcalc(rightLeg,self.rightUpperLeg)
        self.locationRightKnee = rightKnee
        CenterofMass.append(cogRightUpperLeg)
        masses.append(mass)
        # right lower leg calculations
        (cogRightLowerLeg,mass,rightFoot)= self.__legcalc(rightKnee,self.rightLowerLeg,False)
        self.locationRightFoot = rightFoot
        CenterofMass.append(cogRightLowerLeg)
        masses.append(mass)

        # Calculate the placement of the arms and their combined center of mass.
        armMiddle = self.bodyposition + (np.array([0,self.length * self.dic["length_Body"] / 2]))
        (vec,armMiddle) = self.__rotationBodyParts(self.bodyposition,armMiddle,self.torso)
        rightArm = armMiddle - sideLength
        leftArm = armMiddle + sideLength
        self.locationRightShoulder = rightArm
        self.locationLeftShoulder = leftArm

        # right upper arm calculations
        (cogRightUpperArm,mass, rightElbow) = self.__armcalc(rightArm,self.rightUpperArm,True,True)
        self.locationRightElbow = rightElbow
        CenterofMass.append(cogRightUpperArm)
        masses.append(mass)
        # right lower arm calculations
        (cogRightLowerArm,mass,righthand) = self.__armcalc(rightElbow,self.rightLowerArm,False,True)
        self.locationRightHand = righthand
        CenterofMass.append(cogRightLowerArm)
        masses.append(mass)
        # left upper arm calculations
        (cogLeftUpperArm,mass, leftElbow) = self.__armcalc(leftArm,self.leftUpperArm,True,False)
        self.locationLeftElbow = leftElbow
        CenterofMass.append(cogLeftUpperArm)
        masses.append(mass)
        # left lower arm calculations
        (cogLeftLowerArm,mass,lefthand) = self.__armcalc(leftElbow,self.leftLowerArm,False,False)
        self.locationLeftHand = lefthand
        CenterofMass.append(cogLeftLowerArm)
        masses.append(mass)

        # body calculations
        vec = legMiddle - armMiddle
        CenterofMass.append(legMiddle + (vec * self.dic["cog_Body"]))
        masses.append(self.weight * self.dic["weight_Body"])

        # head calculations
        (cogHead,mass,head) = self.__headcalc(armMiddle,self.head)
        self.locationHead = head
        CenterofMass.append(cogHead)
        masses.append(mass)

        return p.getCenterOfMass(CenterofMass,masses)

    def positionchange(self,head=0,torso=0,leftupperarm=0,leftlowerarm=0,rightupperarm=0,rightlowerarm=0,leftupperleg=0,leftlowerleg=0,rightupperleg=0,rightlowerleg=0):
        """ Change the position of the bodyparts in radians and calculate
            its new center of mass."""
        self.head = head * (2*np.pi/360)
        self.torso = torso * (2*np.pi/360)
        self.rightUpperArm = rightupperarm * (2*np.pi/360)
        self.rightLowerArm = rightlowerarm * (2*np.pi/360)
        self.rightUpperLeg = rightupperleg * (2*np.pi/360)
        self.rightLowerLeg = rightlowerleg * (2*np.pi/360)
        self.leftUpperArm = leftupperarm * (2*np.pi/360)
        self.leftLowerArm = leftlowerarm * (2*np.pi/360)
        self.leftUpperLeg = leftupperleg * (2*np.pi/360)
        self.leftLowerLeg = leftlowerleg * (2*np.pi/360)
        self.__getCenterOfMass()


    def setturned(self,value):
        """ Change the viewing direction of the gymnast and calculate its
            new center of mass.
            False: facing the screen
            True: facing the wheel"""
        self.turned = value;
        self.cog = self.__getCenterOfMass()

    def getcog(self):
        """ Get the center of mass."""
        return self.cog

    def getweigth(self):
        """ get the mass of the human."""
        return self.weight

    def rightFootOnMiddel(self,rightpos):
        """ Calculte from the position of the right foot the center of the
            body."""
        translatie = rightpos - self.locationRightFoot
        self.bodyposition = self.bodyposition + translatie
        self.__getCenterOfMass()

    def test_bodypositions(self):
        """ Get the bodypart locations."""
        array = [self.locationHead,self.locationLeftShoulder,self.locationLeftElbow,
                 self.locationLeftHand,self.locationRightShoulder,self.locationRightElbow,
                 self.locationRightHand,self.locationLeftHip,self.locationLeftKnee,
                 self.locationLeftFoot,self.locationRightHip,self.locationRightKnee,
                 self.locationRightFoot]

        return array
