import numpy as  np
import math
import time


"""
t = time.time()
elapsed = time.time() - t
print("creating graph time: ",elapsed)
"""


"""
     == Version 1.06, calculating the distance matrix once and running thorught its indexes
    for 5000 points -> running at 0.015 seconds      
    for 10,000 points -> running at 0.015 seconds    
    for 50,000 points -> running at 2.77 seconds                            
    for 100,000 points -> runnin at 30.6 seconds
"""



class Silhouette:
    def __init__(self):
        self.clustersDictionaryIndexes = dict()
        self.clustersDictionaryVectors = dict()
        self.listAvgSilhouette = []
        self.listVectorsForDistanceMatrix = []
        self.distances = np.zeros(1)
        
        
    def calculateSilhouetteValue(self, dataset, clusters):
        #t = time.time()
        self.createclustersDictionaryIndexes(dataset, clusters)
        #elapsed = time.time() - t
        #print("createclustersDictionaryIndexes time: ",elapsed)
        self.distances = dist(np.array(self.listVectorsForDistanceMatrix))
        
        for cluster in self.clustersDictionaryIndexes:
            self.listAvgSilhouette.append(self.calculateAvgSilhoueteOfCluster(cluster))
        arrayValues = np.array(self.listAvgSilhouette)
        return np.average(arrayValues)
         
        
        
    
    
    def createclustersDictionaryIndexes(self, dataset, clusters):
        #pIndex is the true index of the point in data set
        pIndex = -1
        #index is the point index in the distances matrix
        index = 0
        for cluster in clusters:
            pIndex +=1
            #if the point is a noise point
            if cluster == -1:
                continue
            if (cluster in self.clustersDictionaryIndexes) == False:
                self.clustersDictionaryIndexes.update({cluster : []})
            if (cluster in self.clustersDictionaryVectors) == False:
                self.clustersDictionaryVectors.update({cluster : []})
            self.clustersDictionaryVectors[cluster].append(dataset[pIndex])
            #add the vector for distance matrix calculation
            self.listVectorsForDistanceMatrix.append(dataset[pIndex])
            #the dictionary will use the distance matrix therefore will use the matrix indexes
            self.clustersDictionaryIndexes[cluster].append(index)
            index += 1
            
    
    #Calculate avg S values of the cluster
    def calculateAvgSilhoueteOfCluster(self, clusterNumber):     
        #because the calcualtion is the same for all the cluster member they will all have the same A value
        a = self.calculateClusterAValue(clusterNumber)
        arrayBValues = self.calculateBValues(clusterNumber)
        arraySValues =  np.zeros(len(self.clustersDictionaryIndexes[clusterNumber]))
        for i in range(len(arraySValues)):
            b = arrayBValues[i]
            if a < b:
                arraySValues[i] = 1 - (a / b)
                if math.isnan(arraySValues[i]):
                    x=0
                continue
            if a == b:
                arraySValues[i] = 0
                continue
            arraySValues[i] = (b / a) - 1
            if math.isnan(arraySValues[i]):
                    x=0
        
        return np.average(arraySValues)
        
        
            
        
            
            
        

        
    def calculateClusterAValue(self, clusterNumber):
        #because all the memeber will have the same distance sum we can calculate it only once
        numberOfMembers = len(self.clustersDictionaryIndexes[clusterNumber])
        sumDist = 0
        firstIndex = list(self.clustersDictionaryIndexes[clusterNumber])[0]
        
        for index in self.clustersDictionaryIndexes[clusterNumber]:
            sumDist += self.distances[firstIndex, index]
            
        return sumDist / (numberOfMembers - 1)
        
        

    
    def calculateBValues(self, clusterNumber):   
        arrayBValues = np.array([-1] * len(self.clustersDictionaryIndexes[clusterNumber]))
        arrayIndex = -1
        for index in self.clustersDictionaryIndexes[clusterNumber]:
            distSum = 0
            arrayIndex += 1
            #search for minimum B value from all the clusters
            for cluster in self.clustersDictionaryIndexes:
                if cluster == clusterNumber:
                    continue
                for outSideIndex in self.clustersDictionaryIndexes[cluster]:
                    distSum += self.distances[index, outSideIndex]
                bValue = distSum / (len( self.clustersDictionaryIndexes[cluster]))
                #update minimum B value
                if((arrayBValues[arrayIndex] == -1) or (bValue < arrayBValues[arrayIndex])):
                    arrayBValues[arrayIndex] = bValue
        return arrayBValues
                
                
                
                
        
        
            
        
            
        
        
        
        
        
        
        
    def calcSumOfDistance(self, clusterNumber, pIndex):
        x=0

    


def dist(A):
    m, n = A.shape
    B = A @ A.T
    D = np.diag(B).reshape([1, m])
    return (D.T + D - 2 * B)**0.5