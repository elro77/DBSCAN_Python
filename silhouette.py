import numpy as  np
import math
import time


"""
t = time.time()
elapsed = time.time() - t
print("creating graph time: ",elapsed)
"""


class Silhouette:
    def __init__(self):
        self.clustersDictionaryIndexes = dict()
        self.clustersDictionaryVectors = dict()
        self.listAvgSilhouette = []
        
        
    def calculateSilhouetteValue(self, dataset, clusters):
        t = time.time()
        self.createclustersDictionaryIndexes(dataset, clusters)
        elapsed = time.time() - t
        print("createclustersDictionaryIndexes time: ",elapsed)
        
        for cluster in self.clustersDictionaryIndexes:
            self.listAvgSilhouette.append(self.calculateAvgSilhoueteOfCluster(cluster))
         
        
        
    
    
    def createclustersDictionaryIndexes(self, dataset, clusters):
        pIndex = -1
        for cluster in clusters:
            pIndex +=1
            #if the point is a noise point
            if cluster == -1:
                continue
            if (cluster in self.clustersDictionaryIndexes) == False:
                self.clustersDictionaryIndexes.update({cluster : []})
            if (cluster in self.clustersDictionaryVectors) == False:
                self.clustersDictionaryVectors.update({cluster : []})
            self.clustersDictionaryIndexes[cluster].append(pIndex)
            self.clustersDictionaryVectors[cluster].append(dataset[pIndex])
            
    def calculateAvgSilhoueteOfCluster(self, clusterNumber):     
        arrayAValues = self.calculateAValues(clusterNumber)
        arrayBValues = self.calculateBValues(clusterNumber)
            
            
        

        
    def calculateAValues(self, clusterNumber):
        numberOfMembers = len(self.clustersDictionaryIndexes[clusterNumber])
        listAValues = []
        listBValues = []
        self.arrayValueA = np.zeros(numberOfMembers)
        self.arrayValueB = np.zeros(numberOfMembers)
        distances = dist(np.array(self.clustersDictionaryVectors[clusterNumber]))
        for row in range(distances):
            sumDist = np.sum(row)
            listAValues.append(sumDist/(numberOfMembers - 1))
        return np.array(listAValues)
            
    
    
    def calculateBValues(self, clusterNumber):
        x=0
    def calcSumOfDistance(self, clusterNumber, pIndex):
        x=0

    


def dist(A):
    m, n = A.shape
    B = A @ A.T
    D = np.diag(B).reshape([1, m])
    return (D.T + D - 2 * B)**0.5