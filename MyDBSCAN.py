import numpy as np
import math

class CMyDBSCAN:
    def __init__(self, _size, _eps ,_minPoints):
        #arrays
        self.clusters = [-1] * _size
        self.noisePoints = [False] * _size
        self.undefinedPoints = [True] * _size
        #integers
        self.minPoints = _minPoints
        self.eps = _eps
        self.currnetCluster = -1
        #connections
        self.connectionsDictionary = dict()
        self.gridDictionary = dict()
        
        
        
    def startClustering(self, dataSet):
        self.createGraph(dataSet)
        """
        for pIndex in range(len(dataSet)):
            if(self.undefinedPoints[pIndex] == False):
                continue
            self.connectionsDictionary.update(pIndex,[])
            neighbors = self.rangeQuery(dataSet, pIndex)
            if len(neighbors) < self.minPoints:
                self.noisePoints[pIndex] = True
                self.undefinedPoints[pIndex] = False
                continue
            self.currnetCluster += 1 
            self.clusters[pIndex] = self.currnetCluster
            self.undefinedPoints[pIndex] = False
            neighbors.remove(pIndex)
            seedSet = neighbors[:]
            for qIndex in seedSet:
                seedSet.remove(qIndex) #removing the index inorder to not call it again
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
                    seedSet.remove(qIndex) #removing a neighbor which was already called
        """
   
        return self.clusters
    
    def rangeQuery(self,data, qIndex):
        neighborsList = []
        for pIndex in range(len(data)):
            if (qIndex == pIndex) or (self.calcEuclideanDistance(data, qIndex, pIndex) <= self.eps):
                neighborsList.append(pIndex)     
        return neighborsList
    
    

    def calcEuclideanDistance(self,data, qIndex ,pIndex):
        sm = 0
        p1 = data[qIndex]
        p2 = data[pIndex]
        for i in range(len(p1)):
            sm += (p1[i]-p2[i]) * (p1[i]-p2[i])
        return sm
    
    def createGraph(self,data):
        pointsArray = [[int(i) for i in l] for l in data]
        for pIndex in range(len(data)):
            avg = int(sum(value for value in data[pIndex])/len(data[pIndex]))
            if not (avg in  self.gridDictionary):
                self.gridDictionary.update({avg : []})   
            self.gridDictionary[avg].append(pIndex)
            
            
    
                
    
    
    
    



    

