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

import math
import sympy as sym
#from sympy.plotting import plot

from time import time

from MyConstants import LN

from GetUserInput import getNDimensions, getNParams, getEquation, getErrorType, getData
from NeuralNet import NeuralNet as NN
from FitHelper import getInputLayer, calcDistance


"""
nDimensions = getNDimensions()
nParams = getNParams()
equationData = getEquation(nDimensions, nParams)
paramSymbols = equationData.pop()
dimSymbols = equationData.pop()
equation = equationData.pop()
errorType = getErrorType()
points = getData(nDimensions)

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
once network is sufficiently trained(how to know when this is?)
    plug in 0 as output and back propagate
"""

#init NN with 3 layers of 5, 5, and 1 neurons, respectively
net = NN([5,5,1])

#~~~~~~~~~~~~~~~~~~~~~~repeat this section~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#TODO set bounds on input layer params
#get a new random input layer
inputs = getInputLayer()

#TODO allow for calculating diferent types of distances
#calculate true output
output = calcDistance()

#init input layer neurons' values to 1, 2, 3, 4, and 5
net.setInputLayer([1,2,3,4,5])

#forward calculate activation energies in->hidden(s)->out
net.fCalc();
print(net.strNodeVals())

#calculate actual value

#calculate error

#back propogate

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import random as rand


h = rand.uniform(-100.0,100.0)
k = rand.uniform(-100.0,100.0)
a = rand.uniform(0,1.57)
r = rand.uniform(-100.0,100.0)
p = rand.uniform(-100.0,100.0)

xt = "R*cos(t)*cos(a)-P*sin(t)*sin(a)+h"
yt = "R*cos(t)*sin(a)+P*sin(t)*cos(a)+k"


t = sym.symbols('t')

dxdt = sym.diff(xt, t)
dydt = sym.diff(yt, t)

"(x,y)=10,20"
eqn = "("+str(xt)+"-10)*"+str(dxdt)+"+("+str(yt)+"-20)*"+str(dydt)

eqn = eqn.replace("h",str(h))
eqn = eqn.replace("k",str(k))
eqn = eqn.replace("a",str(a))
eqn = eqn.replace("R",str(r))
eqn = eqn.replace("P",str(p))

tEst = 0
cos = "math.cos"
sin = "math.sin"
eqn = eqn.replace("t",str(tEst))
eqn = eqn.replace("cos",str(cos))
eqn = eqn.replace("sin",str(sin))

t = time()
for i in range (10000):
    eval(eqn)
print(str(time()-t))
"""
equation = "(((x-h)*cos(a)-(y-k)*sin(a))^2)/r+(((x-h)*sin(a)+(y-k)*cos(a))^2)/p-1"


equation = equation.replace("h",str(h))
equation = equation.replace("k",str(k))
equation = equation.replace("a",str(a))
equation = equation.replace("r",str(r))
equation = equation.replace("p",str(p))
print(equation)


X = 1000
Y = 2000

distance = "(x-X)^2+(y-Y)^2-r"

distance = distance.replace("X",str(X))
distance = distance.replace("Y",str(Y))
print(distance)


t = time.time()

y=symbols('y')
r=symbols('r')

sol = solve(distance,y)
print(sol)
equation = equation.replace("y",str(sol[1]))
print(equation)
sol = solve(equation,r)
print(sol)

#sol = solve(equation,y)

print(LN+str(time.time()-t)+" seconds to solve")


print('The minimum distance is {0:1.2f}'.format(objective(X)))
"""
            






















