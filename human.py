gimport numpy as np
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
        #length in cm
        self.length = length
        #weigth in killo's
        self.weight = weight
        # the bodyposition is the posstion of the middle of the body
        self.bodyposition = np.array(bodyposition)
        # the midsize of a shoulder
        self.shoulderSize = shouldersize
        #if the turner is turned
        self.turned = False;
        if "done" not in self.dic.keys():
            self.dic["done"] = 1
            f = open("humaninit.txt",'r')
            for line in f:
                (key,value) = line.split()
                self.dic[key] = float(value)
        self.cog = self.__getCenterOfMass()

    def __rotationBodyParts(self,begin,end,rot):
        """ Here we can rotate a bodypart without knowing the body part by
            using a vector caclulated between de diffrence and the start this will give back
            (vector from start to end, place of end)"""
        vec = end - begin
        vec = np.dot(p.rotation2d(rot),vec)
        end = begin + vec
        return(vec,end)

    def __legcalc(self,topposition,legrot,Upper=True):
        """Caclulate the place of Center of mass and place of the end part
            """
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
        """
        Here we caclulate the arm length and place and cog of arm parts
        """
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
        tophead = neck + np.array([0,self.length * self.dic["length_Head"]])
        (vec,tophead) = self.__rotationBodyParts(neck,tophead,self.head)
        cog = neck + vec * (1 - self.dic["cog_Head"])
        mass = self.weight * self.dic["weight_Head"]
        return(cog,mass,tophead)

    def __getCenterOfMass(self):
        CenterofMass=[]
        masses = []
        # here first we caclulate the place of the legs and there center of mass
        # and put them into
        legMiddle = self.bodyposition - (np.array([0,self.length * self.dic["length_Body"] /2]))
        (vec,legMiddle)= self.__rotationBodyParts(self.bodyposition,legMiddle,self.torso)
        if self.turned:
            sideLength = [0,0]
        else:
            sideLength = [self.shoulderSize/ 2,0]
        rightLeg = legMiddle - sideLength
        leftLeg = legMiddle + sideLength
        # left leg upper caclulations    self.rightUpperLeg = 0
        (cogLeftUpperLeg,mass,leftKnee)= self.__legcalc(leftLeg,self.leftUpperLeg)
        CenterofMass.append(cogLeftUpperLeg)
        masses.append(mass)
        #lower left caclulation
        (cogLeftLowerLeg,mass,leftFoot) = self.__legcalc(leftKnee,self.leftLowerLeg,False)
        CenterofMass.append(cogLeftLowerLeg)
        masses.append(mass)
        #rightUpperLeg caclulations
        (cogRightUpperLeg,mass,rightKnee)= self.__legcalc(rightLeg,self.rightUpperLeg)
        CenterofMass.append(cogRightUpperLeg)
        masses.append(mass)
        #right LowerLeg
        (cogRightLowerLeg,mass,rightFoot)= self.__legcalc(rightKnee,self.rightLowerLeg,False)
        CenterofMass.append(cogRightLowerLeg)
        masses.append(mass)
        # now let's caclulate the arms
        armMiddle = self.bodyposition + (np.array([0,self.length * self.dic["length_Body"] / 2]))
        print(armMiddle)
        (vec,armMiddle) = self.__rotationBodyParts(self.bodyposition,armMiddle,self.torso)


        rightArm = armMiddle - sideLength
        leftArm = armMiddle + sideLength

        (cogRightUpperArm,mass, rightElbow) = self.__armcalc(rightArm,self.rightUpperArm,True,True)
        CenterofMass.append(cogRightUpperArm)
        masses.append(mass)
        (cogRightLowerArm,mass,righthand) = self.__armcalc(rightElbow,self.rightLowerArm,False,True)
        CenterofMass.append(cogRightLowerArm)
        masses.append(mass)
        (cogLeftUpperArm,mass, leftElbow) = self.__armcalc(leftArm,self.rightUpperArm,True,False)
        CenterofMass.append(cogLeftUpperArm)
        masses.append(mass)
        (cogLeftLowerArm,mass,lefthand) = self.__armcalc(leftElbow,self.rightLowerArm,False,False)
        CenterofMass.append(cogLeftLowerArm)
        masses.append(mass)
        #body cacls
        vec = legMiddle - armMiddle
        print(legMiddle)
        print(armMiddle)
        CenterofMass.append(legMiddle + (vec * self.dic["cog_Body"]))
        masses.append(self.weight * self.dic["weight_Body"])

        # head caclc
        (cogHead,mass,head) = self.__headcalc(armMiddle,self.head)
        CenterofMass.append(cogHead)
        masses.append(mass)
        return p.getCenterOfMass(CenterofMass,masses)

    def positionchange(self,head=0,torso=0,leftupperarm=0,leftlowerarm=0,rightupperarm=0,rightlowerarm=0,leftupperleg=0,leftlowerleg=0,rightupperleg=0,rightlowerleg=0):
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
        self.cog = self.__getCenterOfMass()

    def setturned(self,value):
        self.turned = value;
        self.cog = self.__getCenterOfMass()

    def getcog(self):
        return self.cog

    def rightfoodtomiddel(self,rightpos):
        rightKnee =rightpos +  self.length * np.array([0,self.length * self.dic['length_Lower_Leg']])
        (_,rightKnee) = self.__rotationBodyParts(rightpos,rightKnee,np.pi + self.rightLowerLeg)
        rightHip = rightKnee + self,lenght * np.array([0,self.length * self.dic['length_Upper_Leg']])
        (_,rightHip) = self.__rotationBodyParts(rightKnee,rightHip,np.pi + self.rightUpperLeg)
        middle = rightHip + np.array([self.shoulderSize/2,0 ])
        (_,middle) = self.__rotationBodyParts(rightHip,middle,np.pi + self.torso)
        bodymiddle = middle + np.array([0,self.dic['length_Body'] / 2])
        (_,bodymiddle) = self.__rotationBodyParts(middle,bodymiddle,np.pi + self.torso)
        self.bodyposition = bodymiddle


#test code
human = human(180,100,list([0,0]),20)
human.positionchange(torso=20)
print(human.cog)
