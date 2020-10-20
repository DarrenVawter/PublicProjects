# -*- coding: utf-8 -*-

import random as rand
import math

class NeuralNet():

    def __init__(self, networkMap = [5,5,5,1]):
        
        self.nn = []
        self.nn.clear()
        
        for i in range(len(networkMap)):
            layer = []
            layer.clear()
            if(networkMap[i]<0):
                raise Exception("Number of neurons in layer must be positive.")
            for j in range(networkMap[i]):
                if(i==0):
                    layer.append(Neuron(0))
                else:
                    layer.append(Neuron(networkMap[i-1]))
            self.nn.append(layer)

    def __str__(self):
        
        res = "\n"
        moreNodes = True

        j = 0
        while(moreNodes):
            moreNodes = False
            for i in range(len(self.nn)):
                if(len(self.nn[i])>j):
                    moreNodes = True
                    res += "N--"
                else:
                    res += "---"  
            j += 1
            res = res[:len(res)-2] + "\n"
            if(moreNodes):
                for i in range(len(self.nn)):
                    res += "---"
                res = res[:len(res)-2] + "\n"
            else:
                res = res[0:len(res)-6*len(self.nn)+1]
                    
            
        return res
  

    def strNodeVals(self):  
        
        res = "\n"
        for i in range(len(self.nn)*9-3):
            res += "|"
        moreNodes = True
        res += "\n"
        
        j = 0
        while(moreNodes):
            moreNodes = False
            for i in range(len(self.nn)):
                if(len(self.nn[i])>j):
                    moreNodes = True
                    res += str(self.nn[i][j])
                    res += "|||"
                else:
                    res += "|||||||||"
            res = res[:len(res)-3] + "\n"
            j += 1
            if(moreNodes):
                for i in range(len(self.nn)):
                    res += "|||||||||"
                res = res[:len(res)-3] + "\n"
            else:
                res = res[0:len(res)-9*len(self.nn)+1]
        return res

    def setInputLayer(self, inputs):
        
        #verify input is a list
        if(type(inputs) != list):
            raise Exception("Inputs must be a list.")
        #verify input list matches input layer size
        if(len(inputs) != len(self.nn[0])):
            raise Exception("Input list and input layer size must match.")
            
        #assign values to neurons
        for n in range(len(self.nn[0])):
            self.nn[0][n].val = inputs[n]
            
        return

    def fCalc(self):
        
        #For each Layer (except the first)
        for layer in range(1,len(self.nn)):
            #for each Neuron in this layer
            for n in range(len(self.nn[layer])):
                #easier referencing
                neuron = self.nn[layer][n]
                #reset this neuron's activation value
                neuron.val = 0
                #for each connection in this neuron to the previous layer
                for w in range(len(neuron.weights)):
                    #add the weighted value of the connected neuron
                    neuron.val += neuron.weights[w]*self.nn[layer-1][w].val
                #add neuron's bias
                neuron.val += neuron.bias
                #squash activation value
                neuron.val = ( 2 / (1+math.exp(-neuron.val)) ) - 1
                
            

class Neuron():    
    
    def __init__(self, nWeights: int, val=0):
        
            self.val = float(val)
            self.bias = rand.uniform(-1.0,1.0)
            self.weights = []
            self.weights.clear()
            
            for i in range(nWeights):
                self.weights.append(rand.uniform(-1.0,1.0))
                
    def __str__(self):
        if(self.val>=0):
            return "+"+"{:.3f}".format(self.val)
        else:              
            return "{:.3f}".format(self.val)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    