# -*- coding: utf-8 -*-

import random as rand
import math
import numpy as np

class NeuralNet():

    def __init__(self, networkMap = [1,1,1], learningRate = 1):
        
        nLayers = len(networkMap)
                
        self.learnRate = learningRate
        
        self.activationVector = [None]*nLayers
        self.weightMatrix = [None]*nLayers
        self.biasVector =  [None]*nLayers
        self.errorVector = [None]*nLayers

        self.weightDelMatrix = [None]*nLayers
        self.biasDelVector =  [None]*nLayers
        
        #layer 0 remains a None object for all attributes except activation
        self.activationVector[0] = np.zeros(shape=(networkMap[0],1))
        
        #allowing it to exist prevents off-by-1 indexing later on
        for l in range(1,nLayers):
            
            rowsP = networkMap[l-1]
            rows = networkMap[l]
            
            #init activation values to 0 (in case print is called)
            self.activationVector[l] = np.zeros(shape=(rows,1))
            
            #init weight matrices
            self.weightMatrix[l] = (np.random.rand(rowsP,rows)-0.5)*2
            self.weightDelMatrix[l] = np.zeros(shape=(rowsP,rows))
            
            #init biases
            self.biasVector[l] = (np.random.rand(rows,1)-0.5)*2
            self.biasDelVector[l] = np.zeros(shape=(rows,1))
            
            #init errors
            self.errorVector[l] = (np.random.rand(rows,1)-0.5)*2
        
        return
    
    def __str__(self):
        res = "\n"
        for i in range(len(self.activationVector)*11-4):
            res += "|"
        moreNodes = True
        res += "\n"
        
        j = 0
        while(moreNodes):
            moreNodes = False
            for i in range(len(self.activationVector)):
                if(len(self.activationVector[i])>j):
                    moreNodes = True
                    if(self.activationVector[i][j]<0):
                        res += "{:.4f}".format(self.activationVector[i][j,0])
                    else:
                        res += "+{:.4f}".format(self.activationVector[i][j,0])
                    res += "||||"
                else:
                    res += "|||||||||||"
            res = res[:len(res)-4] + "\n"
            j += 1
            if(moreNodes):
                for i in range(len(self.activationVector)):
                    res += "|||||||||||"
                res = res[:len(res)-4] + "\n"
            else:
                res = res[0:len(res)-11*len(self.activationVector)+2]
        return res

    def setInputLayer(self,inputs:list):

        if(inputs is None):
            raise Exception("Input vector cannot be empty list.")
        elif(len(inputs)!=len(self.activationVector[0])):
            raise Exception("Input vector size mismatch.")
        
        #element-wise copy from arg to NN input layer
        for i in range(len(inputs)):
            self.activationVector[0][i] = inputs[i]
        
        return
    
    def getInputLayer(self):
        return self.activationVector[0]
        
    def fCalc(self):
        
        for l in range(1,len(self.weightMatrix)):
            self.activationVector[l] = np.dot(np.transpose(self.weightMatrix[l]),self.activationVector[l-1])
            f = self.activationVector[l]
            self.activationVector[l] = 1/(1+np.exp(-f))
        return
    
    def bCalc():
        return
        
    def bPropagate(self, labelVector:list):
        
        nLayers = len(self.activationVector)
        
        if(labelVector is None):
            raise Exception("Empty label list")
        elif(len(labelVector)!=len(self.activationVector[nLayers-1])):
            raise Exception("Label vector size mismatch")
        
        #calculate output layer error
        self.errorVector[nLayers-1] = (labelVector-self.activationVector[nLayers-1])**2
                
        #calculate error for all preceding layers (except input)
        for l in range(1,nLayers):
            
            layer = nLayers-l
            
            #errorV(previous) = [weight <dot> errorV(current)] <hadamard> sigmoidDerivative
            self.errorVector[layer-1] = np.dot(self.weightMatrix[layer],self.errorVector[layer])
            dSigmoid = np.multiply(1-self.activationVector[layer-1],self.activationVector[layer-1])
            self.errorVector[layer-1] = np.multiply(self.errorVector[layer-1],dSigmoid)
        
        for l in range(1,nLayers):
            
            #calc weight dels
            gradient = np.dot(self.activationVector[l-1],np.transpose(self.errorVector[l]))
            self.weightDelMatrix[l] -= self.learnRate * gradient
        
            #calc bias dels
            gradient = self.errorVector[l]
            self.biasDelVector[l] -= self.learnRate * gradient
        
        return
    
    def endBatch(self, batchSize:int):
        
        if(batchSize<1):
            raise Exception("Batch size must be greater than 0.")

        #reset min batch error to unset flag
        self.savedInputLayer = None

        #adjust dels coefficient 
        coefficient = self.learnRate/(2*batchSize)
              
        #skip the first layer
        nLayers = len(self.activationVector)
        for l in range(1,nLayers):
            
            #multiply dels coefficient in
            self.weightDelMatrix[l] *= coefficient
            self.biasDelVector[l] *= coefficient 
            
            #add dels to actual weight and bias values           
            self.weightMatrix[l] += self.weightDelMatrix[l]
            self.biasVector[l] += self.biasDelVector[l]
        
            #reset dels to 0
            self.weightDelMatrix[l].fill(0)
            self.biasDelVector[l].fill(0)
            
    
    
    
    
    
    
    
    
    
    
    
    