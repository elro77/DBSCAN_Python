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
        self.clusters = [-1] * _size
        self.noisePoints = [False] * _size
        self.undefinedPoints = [True] * _size
        self.actualKeys = set()
        #integers
        self.minPoints = _minPoints
        self.eps = _eps
        self.currnetCluster = -1
        #connections
        self.connectionsDictionary = dict()
        self.gridDictionaryVectors = dict()
        self.gridDictionaryIndexes = dict()
        #distancematrix
        #self.distMatrix = np.zeros((_size, _size), dtype = bool) #problomatic
        
        
        
    def startClustering(self, dataSet):
        self.createGraph(dataSet)
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
    
    
    def algoDBSCAN(self, dataSet):
        for pIndex in dataSet:
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
    
    
    
    def rangeQuery(self,data, qIndex):
        if(qIndex in self.connectionsDictionary) == False:
            return [qIndex]
        return self.connectionsDictionary[qIndex]
    
    

    def calcEuclideanDistance(self,data, qIndex ,pIndex):
        sm = 0
        if(qIndex == pIndex):
            return 0
        p1 = data[qIndex]
        p2 = data[pIndex]  
        temp = p1 - p2
        sm = np.dot(temp.T, temp) ** 0.5
        return sm
    
    def dist(self, A):
        m, n = A.shape
        B = A @ A.T
        D = np.diag(B).reshape([1, m])
        return (D.T + D - 2 * B)**0.5

    
    def createGraph(self,data):
        #create data set that find nearest neighbors
        t = time.time()
        self.initgridDictionaryVectors(data)
        elapsed = time.time() - t
        print("createGraph time: ",elapsed)
        #create a graph of connection with eps distances
        t = time.time()
        self.initGraph(data)
        elapsed = time.time() - t
        print("initGraph time: ",elapsed)
        

    def zipGrid(self):
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
        
        
    def initgridDictionaryVectors(self, data):
        #here we must run through all points and  connect them via map with O(n) only!
        dimentions = len(data[0])
        for pIndex in range(len(data)):
            currentKey = int(np.sum(data[pIndex])/dimentions)   
            self.actualKeys.add(currentKey)
            if (currentKey in  self.gridDictionaryVectors) == False:
                   self.gridDictionaryVectors.update({currentKey : []})   
                   self.gridDictionaryIndexes.update({currentKey : []})   
            self.gridDictionaryVectors[currentKey].append(data[pIndex])
            self.gridDictionaryIndexes[currentKey].append(pIndex)
        #t = time.time()
        self.zipGrid()
        #elapsed = time.time() - t
        #print("zip grid time: ",elapsed)
        
    def connectNodes(self, key, pIndex, qIndex):
        realPIndex = self.gridDictionaryIndexes[key][pIndex]
        realQIndex = self.gridDictionaryIndexes[key][qIndex]
        if (realPIndex in self.connectionsDictionary) == False:
            self.connectionsDictionary.update({realPIndex : set()})
        self.connectionsDictionary[realPIndex].add(realQIndex)
        if (realQIndex in self.connectionsDictionary) == False:
            self.connectionsDictionary.update({realQIndex : set()})
        self.connectionsDictionary[realQIndex].add(realPIndex) 
               
        
                
    def initGraph(self, data):
        cnt = 0
        for key in self.actualKeys:
            #cnt+=1
            #print("#",cnt)
            #t = time.time()
            t = time.time()
            result = self.dist(np.array(self.gridDictionaryVectors[key]))
            #elapsed = time.time() - t
            #print("dist calc : ",elapsed)
            
            #t = time.time()
            #mat is the valid connections
            mat = result <= self.eps
            
            arrayOfTrueAmounts = np.sum(mat,axis=1)
            arrayCheck = arrayOfTrueAmounts >= self.minPoints
            arrayValid = np.where(arrayCheck)[0]
            
            pIndex = -1
            for row in arrayValid:
                #t__ = time.time()
                pIndex += 1
                trueAmounts = np.sum(row)
                if trueAmounts >= self.minPoints:
                    #try to modify here                 
                    #save this list as connections
                    indexses = np.where(mat[row])[0]
                
                
                    #elapsed = time.time() - t__
                    #print("time passed for row #" ,cRow, ": ",elapsed)
                    #print("time passed for np where #" ,row, ": ",elapsed)
                    #t__ = time.time()
                    #self.connectNodes(key, row, indexses) 
                    realPIndex = self.gridDictionaryIndexes[key][pIndex]
                    listIndexes = []
                    listIndexes = [self.gridDictionaryIndexes[key][qIndex] for qIndex in indexses]
                    listIndexes.append(realPIndex)
                    if (realPIndex in self.connectionsDictionary) == False:
                        self.connectionsDictionary.update({realPIndex : []})
                        self.connectionsDictionary[realPIndex] += listIndexes
                
                
                #elapsed = time.time() - t__
                #print("time passed for insertion #" ,row, ": ",elapsed)
            #self.algoDBSCAN(self.gridDictionaryIndexes[key])
            #self.connectionsDictionary.clear()
            elapsed = time.time() - t
            print("time passed for key" ,key, ": ",elapsed)
                     
                
        
            
            

            
            
    
                
    
    
    
    



    


