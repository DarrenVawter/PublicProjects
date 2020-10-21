# -*- coding: utf-8 -*-

"""
Code written by Darren Vawter
(14OCT20-current)

Github link:
"""

"""
user specifies spatial dimensions
	[1,2,3] --> [x,x&y,x&y&z]
	-start with just x&y
user enters # of adjustment parameters
	[1,2,3,4,...,21,22,23] --> [a,b,c,d,...,t,u,v]
	-determine max # parameters for reasonable performance?
	-warn users about low time efficiency with many parameters
    -0 parameters implies the user only wants an error rating
user enters equation
	-parse equation & verify that no illegal dimensions or parameters were used
user enters type of error to minimize
	[min/max/mean/median/mode (x,y,z,xy,xz,yz,xyz)delta raws/squares/quartics]
user enters list of points
	-parse list of points
	-validate list of points 
begin processing algorithm
"""

from time import time

import numpy as np

#from sympy.plotting import plot

from MyConstants import LN

from GetUserInput import getNDimensions, getNParams, getEquation, getErrorType, getData
from NeuralNet import NeuralNet as NN
from FitHelper import generateInputLayer, calcError

def squashList(vector:list):
    vector2 = []
    vector2.clear()
    for i in range(len(vector)):
        vector2.append(1/(1 + np.exp(-vector[i]))) 
    return vector2

#skipping dynamic input for now for faster testing
"""
nDimensions = getNDimensions()
nParams = getNParams()
equationData = getEquation(nDimensions, nParams)
errorType = getErrorType()
points = getData(nDimensions)

paramSymbols = equationData.pop()
dimSymbols = equationData.pop()
equation = equationData.pop()

print(LN+str(nDimensions))
print(nParams)
print(equationData)
print(errorType)
print(points)
"""

"""
5x5x5x1
map params to ouputs
network error is difference between output and error function
once network is sufficiently trained (how to know when this is?)
plug in 0 as output and back calculate
"""

#init NN with 3 layers of 5, 5, and 1 neurons, respectively
net = NN([5,5,5,5,1])

#static init equations
xT = "R*cos(T)*cos(a)-P*sin(T)*sin(a)+h"
yT = "R*cos(T)*sin(a)+P*sin(T)*cos(a)+k"

#static init data points
points = [[-1,0],[1,0],[0,1],[0,-1]]

#declare how much training to perform
nBatches = 10
batchSize = 10000
paramEstimates = [0,0,0,1,1]
estimatesDoubt = [1,1,2,1,1]
tParamEstimates = [0,0,0,0,0]
minTrueError = None

timerStart = time()
for batch in range(nBatches):
    
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~mini batch~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    batchStart = time()
    batchCost = 0
    print("Starting batch: "+str(batch+1))
    for trial in range(batchSize+1):
        
        #TODO: set bounds on input layer params dynamically
        #get a new random input layer
        inputLayer = generateInputLayer(paramEstimates,estimatesDoubt)
        
        #label true error based on generated input parameters
        trueError = calcError([xT,yT],inputLayer,points)
        #check if this is a new minimum true error
        if(minTrueError is None or trueError<minTrueError):
            minTrueError = trueError
            tParamEstimates.clear()
            for p in range(len(inputLayer)):
                tParamEstimates.append(inputLayer[p])
        #squash the true error for 1:1 comparison
        trueError = 1/(1 + np.exp(-trueError)) 
        
        #set input layer neurons' values to generated init parameters
        net.setInputLayer(squashList(inputLayer))
            
        #forward calculate activation energies in->hidden(s)->out
        net.fCalc();
        
        #back propogate
        net.bPropagate([trueError])
        
        #add to running batch error sum
        batchCost += net.errorVector[4][0]
        
        if(trial%500==0):
            print("{:.0f}".format(100*trial/batchSize)+"%")        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #get average error by dividing by batchSize
    batchCost /= batchSize
    #get best guess values from min error result
    paramEstimates.clear()
    for p in range(len(tParamEstimates)):
        paramEstimates.append(tParamEstimates[p])
        #update confidence
        estimatesDoubt[p] *= 0.9
    #set new doubt level
    #TODO: make this a per-param setting
    batchEnd = time()
    print("Batch "+str(batch+1)+" avg cost: "+str(batchCost))
    print("Batch time: "+str(batchEnd-batchStart)+" seconds")
    print(paramEstimates)
    print("Min params error: "+str(calcError([xT,yT],paramEstimates,points)))
    print("\n")
    net.endBatch(batchSize)

timerEnd = time()


net.fCalc();
print("Timer: "+str(timerEnd-timerStart)+" seconds")














