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
        #integers
        self.minPoints = _minPoints
        self.eps = _eps
        self.currnetCluster = -1
        #connections
        self.connectionsDictionary = dict()
        self.gridDictionary = dict()
        #distancematrix
        #self.distMatrix = np.zeros((_size, _size), dtype = bool) #problomatic
        
        
        
    def startClustering(self, dataSet):
        self.createGraph(dataSet)
        t = time.time()
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
        elapsed = time.time() - t
        print("DBSCAN run time: ",elapsed)
        return self.clusters
    
    def rangeQuery(self,data, qIndex):
        """
        neighborsList = []
        for pIndex in range(len(data)):
            if (qIndex == pIndex) or (self.calcEuclideanDistance(data, qIndex, pIndex) <= self.eps):
                neighborsList.append(pIndex)   
        """
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
    
    def createGraph(self,data):
        #create data set that find nearest neighbors
        self.initGridDictionary(data)
        #create a graph of connection with eps distances
        self.initGraph(data)
        
    def initGridDictionary(self, data):
        #here we must run through all points and  connect them via map with O(n) only!
        pointsArray = [[int(i) for i in l] for l in data]
        for pIndex in range(len(data)):
            avg = int(sum(value for value in data[pIndex])/len(data[pIndex]))
            for key in range(avg - self.eps, avg + self.eps):
                if key < 0:
                    continue
                if (key in  self.gridDictionary) == False:
                    self.gridDictionary.update({key : []})   
                self.gridDictionary[key].append(pIndex)
                
                
    def initGraph(self, data):
        for key in self.gridDictionary:
            print("start key: ",key)
            t = time.time()
            for pIndex in range(len(self.gridDictionary[key])):
                for qIndex in range(pIndex + 1, len(self.gridDictionary[key])):
                    p = self.gridDictionary[key][pIndex]
                    q = self.gridDictionary[key][qIndex]
                    if p in self.connectionsDictionary:
                        if q in self.connectionsDictionary[p]:
                            continue
                    if self.calcEuclideanDistance(data, self.gridDictionary[key][pIndex], self.gridDictionary[key][qIndex]) <= self.eps:
                        
                        if (p in self.connectionsDictionary) == False:
                            self.connectionsDictionary.update({p : [p]})
                        if (q in self.connectionsDictionary) == False:
                            self.connectionsDictionary.update({q : [q]})
                            
                        self.connectionsDictionary[p].append(q)
                        self.connectionsDictionary[q].append(p)
            elapsed = time.time() - t
            print("time passed for key" ,key, ": ",elapsed)

                        
            
                             

                          
                     
                
        
            
            

            
            
    
                
    
    
    
    



    


