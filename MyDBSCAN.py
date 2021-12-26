import numpy as np
import math
import time

"""
t = time.time()
elapsed = time.time() - t
print("creating graph time: ",elapsed)
"""



class CMyDBSCAN:
    def __init__(self, _size, _eps ,_minPoints):
        #arrays
        self.clusters = [-1] * _size #list for the cluster of each point
        self.noisePoints = [False] * _size #list of noise poiunts
        self.undefinedPoints = [True] * _size #list of points which are not yet classified
        self.actualKeys = set() #actual key is an acutal grid index
        #integers
        self.minPoints = _minPoints
        self.eps = _eps
        self.currnetCluster = -1
        #connections
        self.connectionsDictionary = dict() #connection betwen pIndex (key) and its neighbors (list)
        self.gridDictionaryVectors = dict() #dictionary for pIndex and its vector
        self.gridDictionaryIndexes = dict() #dicionary for gridPoint(key) and its indexes list

        
        
    #this function will create a graph and run DBSCAN through it    
    def startClustering(self, dataSet):
        self.createGraph(dataSet)
        
        #classify each point in the dataset accoridng to DBSCAN
        for pIndex in range(len(dataSet)):
            if(pIndex in self.connectionsDictionary) == False:
                continue
            if(self.undefinedPoints[pIndex] == False):
                continue
    
            neighbors = self.rangeQuery(dataSet, pIndex)
            if len(neighbors) < self.minPoints:
                self.noisePoints[pIndex] = True
                self.undefinedPoints[pIndex] = False
                continue
            self.currnetCluster += 1 
            self.clusters[pIndex] = self.currnetCluster
            self.undefinedPoints[pIndex] = False
            seedSet = neighbors[:]
            for qIndex in seedSet:
                if self.noisePoints[qIndex] == True:
                    self.noisePoints[qIndex] = False
                    self.clusters[qIndex] = self.currnetCluster
                if self.undefinedPoints[qIndex] == False:
                    continue
                self.clusters[qIndex] = self.currnetCluster
                self.undefinedPoints[qIndex] = False
                qNeighbors = self.rangeQuery(dataSet, qIndex)
                if len(qNeighbors) >= self.minPoints:
                    seedSet.extend(qNeighbors)
        return self.clusters
   
    #will return the neighbors array of pIndex   
    def rangeQuery(self,data, qIndex):
        if(qIndex in self.connectionsDictionary) == False:
            return [qIndex]
        return self.connectionsDictionary[qIndex]
    
    #calculates the distance matrix on A array
    def dist(self, A):
        m, n = A.shape
        B = A @ A.T
        D = np.diag(B).reshape([1, m])
        return (D.T + D - 2 * B)**0.5

    #create the grid and connection path
    def createGraph(self,data):
        #create the index grid of the points
        t = time.time()
        self.initgridDictionaryVectors(data)
        elapsed = time.time() - t
        #print("createGraph time: ",elapsed)
        
        #create a graph of connection with eps distances
        t = time.time()
        self.initGraph(data)
        elapsed = time.time() - t
        #print("initGraph time: ",elapsed)
        
    #this function will unite vectors between each grid groups according to eps
    def zipGrid(self):
         #for each grid point we wil search the connections of its members
         for currentKey in self.actualKeys:
             for key in range(currentKey - self.eps, currentKey - self.eps):
                 if(key < 0) or (currentKey == key):
                     continue
                 if(key in self.actualKeys) == False:
                     continue
                 self.gridDictionaryVectors[currentKey] += self.gridDictionaryVectors[key]
                 self.gridDictionaryIndexes[currentKey] += self.gridDictionaryIndexes[key]
                 
                 self.gridDictionaryVectors[key] += self.gridDictionaryVectors[currentKey]
                 self.gridDictionaryIndexes[key] += self.gridDictionaryIndexes[currentKey]
        
        
    #this function will create an index grid to reduce calculations
    #where each group will be a single value which is calulcated as the avg of all dimentions values
    def initgridDictionaryVectors(self, data):
        dimentions = len(data[0])
        for pIndex in range(len(data)):
            #find the grid point of pIndex
            currentKey = int(np.sum(data[pIndex])/dimentions)  
            self.actualKeys.add(currentKey)
            if (currentKey in  self.gridDictionaryVectors) == False:
                   self.gridDictionaryVectors.update({currentKey : []})   
                   self.gridDictionaryIndexes.update({currentKey : []})   
            self.gridDictionaryVectors[currentKey].append(data[pIndex])
            self.gridDictionaryIndexes[currentKey].append(pIndex)
        #unite nehighbor vectors of other grid points according to eps    
        self.zipGrid()
        
    #this function will loop thourgh the grid and create a graph           
    def initGraph(self, data):
        #for each grid point we wil search the connections of its members
        for key in self.actualKeys:
            t = time.time()
            #calculate distance between all member points to each other
            result = self.dist(np.array(self.gridDictionaryVectors[key]))
            #calculate where are valid connections according to eps (mat)
            mat = result <= self.eps
            #calculate amount of true connections at each row
            arrayOfTrueAmounts = np.sum(mat,axis=1)
            #search for valid rows that has at least minPts (arrayCheck)
            arrayCheck = arrayOfTrueAmounts >= self.minPoints
            #arrayValid will hold array of indexes with atleast minPts connections
            arrayValid = np.where(arrayCheck)[0]
            
            pIndex = -1
            #for each valid index in arrayValid, connect them
            for row in arrayValid:
                pIndex += 1
                trueAmounts = arrayOfTrueAmounts[row]
                if trueAmounts >= self.minPoints:
                    #try to modify here                 
                    #pull colomns indexes with true
                    indexses = np.where(mat[row])[0]
                    #connect between them
                    realPIndex = self.gridDictionaryIndexes[key][row]
                    listIndexes = []
                    listIndexes = [self.gridDictionaryIndexes[key][qIndex] for qIndex in indexses]
                    listIndexes.append(realPIndex)
                    if (realPIndex in self.connectionsDictionary) == False:
                        self.connectionsDictionary.update({realPIndex : []})
                        self.connectionsDictionary[realPIndex] += listIndexes
                
            
                     
                
        
            
            

            
            
    
                
    
    
    
    



    


