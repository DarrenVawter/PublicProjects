# -*- coding: utf-8 -*-
"""
    prompts the user to enter 1, 2, or 3 dimensions
    validates input
        invalid --> retries prompt
        valid --> returns
"""
def getNDimensions():
    
    "return val"
    nDimensions = 0
    
    "fxn internal vars"
    validInput=False
    
    while(not validInput):
        
        "init val & prompt user"
        userInput = input('Enter the number of dimensions (1,2,3): ')
        
        "verify that input is a number"
        try:
            nDimensions = int(userInput)     
        except ValueError:
            try:
                nDimensions = float(userInput)        
            except ValueError:
                print("Valid number of dimensions is 1, 2, or 3.")
                continue  
            
        "verify that a legal nDimensions was chosen"
        "TODO: add 1 and 3 as legal dimensions once viable"
        if(nDimensions == 2):
            validInput = True
        else:
            print("Valid number of dimensions is 1, 2, or 3.")
            
    "return validated result"
    return int(nDimensions)

"""
    prompts the user to enter a legal number of parameters
    validates input
        invalid --> retries prompt
        valid --> returns
"""
def getNParams():
        
    "return val"
    nParams = 0
    
    "fxn internal vars"
    validInput=False
    
    while(not validInput):
        
        "init val & prompt user"
        userInput = input('Enter the number of parameters (0-5): ')
        
        "verify that input is an int"
        try:
            nParams = int(userInput)     
        except ValueError:
            print("The number of parameters must be an integer.")
            continue

        "verify that a legal nParams was chosen"
        if(nParams>5):
            print("The maximum number of parameters is currently 5.")
        elif(nParams<1):
            print("The number of parameters must be non-negative.") 
        else:
            validInput = True

    "return validated result"
    return nParams

"""
    args
        nDimensions: #nDimensions in eqn(assumed to be int)
        nParameters: #nParameters in eqn(assumed to be int)
    prompts the user to enter the equation to fit the data to
    validates input
        invalid --> retries prompt
        valid --> returns
"""
from BinaryTree import Node
def getEquation(nDimensions: int, nParameters: int):
    
    "return val"
    equationData = []
    
    "fxn internal vars"
    validInput=False
    
    while(not validInput):
        
        "init val & prompt user"
        userInput = input('Enter the 0-error equation of the surface: ')
        #TODO: check for spaces between numbers (e.g. <3+2 5+7> )
        "strip whitespace and new lines and change brackets to parens"
        userInput.strip()
        userInput.replace("\n","")
        userInput.replace("[","(")
        userInput.replace("]",")")
        userInput.replace("{","(")
        userInput.replace("}",")")
        userInput = userInput.lower()

        try:
            "if parseNode passes without exception, userInput format is valid"
            parseNode(Node(userInput))   
            
            "if validateSymbols passed without exception, userInput is valid"      
            res = validateSymbols(userInput, nDimensions, nParameters)
            paramSyms = res.pop()
            dimSyms = res.pop()
            
            equationData = [userInput,dimSyms,paramSyms]
            
            "set flag"
            validInput = True
            
        except Exception as e:
            print(e)
            
    return equationData

"""
    args
        node: the node, assumed to have string as its val, to be parsed
    recursively splits the val into children nodes to ensure that it is legal
"""
def parseNode(node: Node):
    
    #print("Parsing: " + node.val)
    
    strLen = len(node.val)
    
    #scan outtermost parend indicies
    opi = getOutterParendIndicies(node.val)
    
    #if outtermost parend indices are start/end --> strip them and reparse
    if(len(opi)==2 and opi[0]==0 and opi[1]==strLen-1):
        node.val = node.val[1:strLen-1]
        parseNode(node)
        return
                
    #create parse tree by parsing in reverse order of operations
        
    #scan for +, -
    split = scanSplit(node.val,opi,"+-")
    if(split!=-1):
        splitNode(node,split)
        return

    #scan for *, /
    split = scanSplit(node.val,opi,"*/")
    if(split!=-1):
        splitNode(node,split)
        return
    
    #scan for ^
    split = scanSplit(node.val,opi,"^")
    if(split!=-1):
        splitNode(node,split)
        return
    
    return
                
"""
returns a list of string indicies indicating the 
ng and closing indicies
of the outtermost parends in the equation.
list odd indicies: opening parends
list even indicies: closing parends corresponding to previous index's opening

"""
def getOutterParendIndicies(eqn:str):
    
    if(eqn is None):
        raise Exception("Empty equation string.")
        
    opi = []

    nOpening = 0
    nClosing = 0
    
    for i in range (len(eqn)):
        
        if(eqn[i]=='('):
            if(nOpening==nClosing):
                opi.append(i)
            nOpening += 1
        elif(eqn[i]==')'):
            nClosing += 1
            if(nOpening==nClosing):
                opi.append(i)
    
    return opi
           
"""
scans the given equation, eqn, for any of the legal characters contained in
string, legal, but skips any indicies bounded by the opi (see above)
"""
def scanSplit(eqn:str,opi:list,legal:str): 
            
    if(eqn is None):
        raise Exception("Empty equation string.")
        
    if(legal is None):
        raise Exception("No legal characters cited.")
        
    if(len(opi)%2==1):
        raise Exception("Invalid Outter Parend Indicies.")

    strLen = len(eqn)

    #if opi is empty, scan the whole string (no parends in eqn)
    if(len(opi)==0):
        for char in range(strLen):
            if(eqn[char] in legal):
                return char
        return -1
    
    #if opi is not empty --> make a copy so as not to alter the original opi
    opiC = opi.copy()   
        
    #init first 'closing parend' index to 0, so the loop will scan 0:first open
    closeI = 0
    #declare next opening parend for while loop
    nextOpenI = 0
    
    #continue to scan sections until next 'open parend' is the end of string
    while(nextOpenI!=strLen):
        #pop the index of the next opening parend (scan:TO for this iter)
        if(len(opiC)>0):
            nextOpenI = opiC.pop(0)
        else:
            nextOpenI = strLen
            
        #verify parend indicies are logical
        if(closeI>nextOpenI):
            raise Exception("Invalid Outter Parend Indicies.")
                        
        #scan for legal chars between bounds
        for char in range(closeI+1,nextOpenI):
            if(eqn[char] in legal):
                return char
            
        #pop the index of the next closing parend (scan:FROM for next iter)
        if(len(opiC)>0):
            closeI = opiC.pop(0)

    #no legal chars were found between parends
    return -1

"""
Splits the node at the given split index, left of index will become left child 
and right of index will become right child. Split index will become val. Then
calls parse on each child node.
"""
def splitNode(node:Node, split:int):

    #split val apart into it's left, right, and (now fully parsed) parent
    node.left = Node(node.val[:split])
    node.right = Node(node.val[split+1:])
    node.val = node.val[split]

    #print("\nSplit:\n"+node.left.val+" <<< "+node.val+" >>> "+node.right.val+"\n")
    
    #parse children
    parseNode(node.left)
    parseNode(node.right)

"""
    args
        equation: the equation str to validate
        dimensions: #nDimensions in eqn(assumed to be int)
        parameters: #nParameters in eqn(assumed to be int)
    ensures that all symbols follow legal placement (no adjacent symbols) and
    that the number of dimension/parameter symbols do not exceed the 
    alloted number of dimensions/parameters
"""
def validateSymbols(equation: str, nDimensions: int, nParameters: int):
    
    "return val"
    symbols = []
    
    "fxn internal vars"
    dimSymbols = ""
    paramSymbols = ""
    strLen=len(equation)
    
    "artificial for loop"
    "starting @ -1 allows increment to be at the top for better readability"
    i = -1
    while (i+1<strLen):
        i+=1

        char = equation[i].lower()
        "check for illegal/legal symbol sequences"
        if(i+4<strLen and char=='a'):
                "acos/asin/atan"
                substr=equation[i:i+4].lower()
                if(substr=="acos" or substr=="asin" or substr=="atan"):
                   i+=3
                   continue;
        if(i+3<strLen):
            if(char=='s'):
                "sin"
                substr=equation[i:i+3].lower()
                if(substr=="sin"):
                   i+=2
                   continue;
            elif(char=='c'):
                "cos"
                substr=equation[i:i+3].lower()
                if(substr=="cos"):
                   i+=2
                   continue;
            elif(char=='t'):
                "tan"
                substr=equation[i:i+3].lower()
                if(substr=="tan"):
                   i+=2
                   continue;
        if(i+1<strLen and char.isalpha()):
                if(equation[i+1].isalpha()):
                    raise Exception("Illegal symbol sequence: ("+char+equation[i+1]+")")                
            
        "track dimension and parameter symbols"
        if(char=='x' or char=='y' or char=='z'):
            if(char not in dimSymbols):
                dimSymbols = dimSymbols + char + ","
                if(len(dimSymbols.split(","))-1>nDimensions):
                    raise Exception("Number of dimension symbols exceeds number"
                                    +" of dimensions: ("+str(nDimensions)+")")
        elif(char.isalpha()):
            if(char not in paramSymbols):
                paramSymbols = paramSymbols + char + ","
                if(len(paramSymbols.split(","))-1>nParameters):
                    raise Exception("Number of parameter symbols exceeds number of"
                                    +" of parameters: ("+str(nParameters)+")")

    "trim excess comma if needed then return each symbol list"
    if(len(dimSymbols)>1):
        dimSymbols = dimSymbols[:len(dimSymbols)-1]
    else:
        dimSymbols = "-1"
    if(len(paramSymbols)>1):
        paramSymbols = paramSymbols[:len(paramSymbols)-1]
    else:
        paramSymbols = "-1"
    symbols = [dimSymbols,paramSymbols]
    return symbols

"""
    prompts the user to enter the error type
    validates input
        invalid --> retries prompt
        valid --> returns
"""
"TODO --> make this more robust or split into 3 fxns instead of being lazy"
def getErrorType():
    
    "return val"
    errorTypes = {}
    
    "fxn internal vars"
    validInput=False
    
    while(not validInput):
        
        "init val & prompt user"
        userInput = input('Enter the desired error type: ')
        
        "Just doing a lazy temporary check here...."
        errorTypes = userInput.split()
        if(len(errorTypes)==3):
            validInput = True

    "return validated result"
    return errorTypes

"""
    prompts the user to enter the list of data points to fit the equation to
    validates input
        invalid --> retries prompt
        valid --> returns
"""
def getData(nDimensions: int):
    
    "return val"
    data = [[]]
    
    "fxn internal vars"
    validInput=False
    
    while(not validInput):
        data.clear()
        
        "init val & prompt user"
        userInput = input("Enter the data to fit: ")
        userInput.strip()
        if(userInput[0]!="("):
            print("Expected: '(' ("+userInput[0]+")")
            continue
        points = userInput.split("(")
        
        try:
            for i in range(len(points)-1):
                dataPoint = []
                dataPoint.clear()
                "check for right parentheses"
                if(points[i+1][len(points[i+1])-1]==")"):
                    points[i+1] = points[i+1][0:len(points[i+1])-1]
                else:
                    raise Exception("Invalid format: ("+points[i+1][0:len(points[i+1])])
                point = points[i+1].split(",")
                "ensure each point is the proper dimension"
                if(len(point)==nDimensions):
                    for j in range(len(point)):
                        dataPoint.append(float(point[j]))
                    data.append(dataPoint)
                else:
                    raise Exception("Data-dimension mismatch ("+points[i+1]+")")
                    
            validInput = True
        except ValueError as e:
            invalidData = e.args[0].split("'")[1]
            print("Invalid data: ("+invalidData+")")
        except Exception as e:
            print(e.args[0])

    "return validated result"
    return data
























