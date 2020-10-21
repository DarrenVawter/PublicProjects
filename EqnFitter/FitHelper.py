# -*- coding: utf-8 -*-

import math
import numpy as np
    
#TODO: this fxn should check bounds on each param
#TODO: this fxn should check how many params are needed for the layer
#TODO: inplement doubt
def generateInputLayer(paramEstimates:list,estimatesDoubtList):
    
    h = np.random.normal(paramEstimates[0], estimatesDoubtList[0])
    k = np.random.normal(paramEstimates[1], estimatesDoubtList[1])
    a = np.random.normal(paramEstimates[2], estimatesDoubtList[2])
    r = np.random.normal(paramEstimates[3], estimatesDoubtList[3])
    p = np.random.normal(paramEstimates[4], estimatesDoubtList[4])
    
    return [h,k,a,r,p]

#TODO: implement other types of error (current is just mean raw xy distance)
#TODO: calc nSteps by asking user for desired resolution
def calcError(eqns:list, inputs:list, points:set):  
    
    if(len(eqns)==0):
        raise Exception("Error: No equations to calc distance from.")
    elif(len(points)==0):
        raise Exception("Error: No equations to calc distance.")
    elif(len(points[0])!=len(eqns)):
        raise Exception("Error: Dimension-mismatch between equations and points.")
        
    #output
    error = 0    
    
    #TODO: add other options here....
    #TODO: need to protect cos and sin from being parsed as params
    cos = "math.cos"
    sin = "math.sin"
    
    #plug in param vals to be tested
    for e in range(len(eqns)):
        
        #TODO: make this dynamic
        eqns[e] = eqns[e].replace("h",str(inputs[0]))
        eqns[e] = eqns[e].replace("k",str(inputs[1]))
        eqns[e] = eqns[e].replace("a",str(inputs[2]))
        eqns[e] = eqns[e].replace("R",str(inputs[3]))
        eqns[e] = eqns[e].replace("P",str(inputs[4]))
        eqns[e] = eqns[e].replace("cos",str(cos))
        eqns[e] = eqns[e].replace("sin",str(sin))
    
    #estimate avg raw xy distance
    avgDist = 0
    for p in range(len(points)):
        
        #get tBounds dynamically
        nSteps = 35
        tBoundU = 2*math.pi
        tBoundL = 0
        tBoundD = tBoundU-tBoundL
        boundManip = 0.9999999999
                
        #if shape is convex, use this to estimate:
        tLast = None
        for step in range(0, int(nSteps/2)):
            
            #1st quartile point
            #determine delta in each dimension and sum squares
            t1Q = tBoundL + 0.25*tBoundD
            t1QD = 0
            for e in range(len(eqns)):
                eq = eqns[e].replace("T",str(t1Q))
                t1QD += (points[p][e]-eval(eq))**2
                        
            #3rd quartile point
            #determine delta in each dimension and sum squares
            t3Q = tBoundL + 0.75*tBoundD
            t3QD = 0
            for e in range(len(eqns)):
                eq = eqns[e].replace("T",str(t3Q))
                t3QD += (points[p][e]-eval(eq))**2
             
            if(tLast is not None and t1QD>tLast and t3QD>tLast):
                #new bounds are inner half
                tBoundU = tBoundL + 0.75*tBoundD
                tBoundL = tBoundL + 0.25*tBoundD
                tBoundD = tBoundU - tBoundL
            elif(t1QD<t3QD):
                #new bounds are lower half
                tBoundU = tBoundL + 0.5*tBoundD
                tBoundD = tBoundU - tBoundL
                tLast = t1QD
            elif(t3QD<t1QD):
                #new bounds are upper half
                tBoundL = tBoundL + 0.5*tBoundD
                tBoundD = tBoundU - tBoundL
                tLast = t3QD
            else:
                #manip ONLY bound delta slightly and try again
                tBoundD *= boundManip
                tLast = t1QD
        
        #add distance to running sum
        if(t1QD<t3QD):
            avgDist += math.sqrt(t1QD)
        else:
            avgDist += math.sqrt(t3QD)
        
        #if shape is concave (or ambiguous), use this to estimate:
        """
        minDist = -1
        for step in range(0, nSteps):
            tVal = tBoundD*step + tBoundL
            eqn = eFxn.replace("t",str(tVal))
            dist = eval(eqn)
            if(dist<)
        avgDist += 
        """  
        
    
    avgDist /= len(points)
    
    error = avgDist
    
    return error

"""
#ANTIQUATED
Takes a list of equation, as strings and calculates/returns their partial
derivatives with respect to t.
def calcPartialDerivatives(eqns:list):

    #output
    partials = []
    partials.clear()
    
    #define parameter to differentiate by
    T = sym.symbols('T')
    
    #calculate partials
    for e in range(len(eqns)):
        partials.append(sym.diff(eqns[e],T))

    #return
    return partials
"""

