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
        self.clusterGravityPointDictionary = dict()
        self.clusterPairsDictionary = dict()
        self.listAvgSilhouette = []
        self.listVectorsForDistanceMatrix = []
        self.distances = np.zeros(1)
        
    #this function will create the gravity point and calculate the S value of the cluster
    def calculateSilhouetteValue(self, dataset, clusters):
        t = time.time()
        #create a map for each cluster with their members
        self.createclustersDictionaryIndexes(dataset, clusters)
        elapsed = time.time() - t
        #print("createclustersDictionaryIndexes() time: ",elapsed)
        
        t = time.time()
        #clculate the graivty points of each cluster
        self.createClusterGravityPoint()
        elapsed = time.time() - t
        #print("createClusterGravityPoint() time: ",elapsed)
        if len(self.clusterGravityPointDictionary) == 0:
            return -1
        t = time.time()
        #find the closest grviatyPoint of each other
        self.findClusterPairs()
        elapsed = time.time() - t
        #print("findClusterPairs() time: ",elapsed)


        t = time.time()
        #calculate any silhoueete value of each cluster using threads
        for cluster in self.clustersDictionaryIndexes:
            self.listAvgSilhouette.append(self.calculateAvgSilhoueteOfCluster(cluster))
        arrayValues = np.array(self.listAvgSilhouette)
        elapsed = time.time() - t
        #print("silhueete total calc  time: ",elapsed)
        return np.average(arrayValues)
         
          
    #create cluster dictionary with their members
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
            #add the index and vector of such cluster
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
            
    #clculate the graivty points of each cluster
    #a cluster gravity point will be calulated as the average point of all it's member points        
    def createClusterGravityPoint(self):
        #for each cluster
        for key in self.clustersDictionaryVectors:
            pointsArray = np.array(self.clustersDictionaryVectors[key])
            #calculate average of all colomns
            clusterPoint = pointsArray.mean(0) 
            if(key in self.clusterGravityPointDictionary) == False:
                self.clusterGravityPointDictionary.update({key : clusterPoint})
                
    #find the closest grviatyPoint of each other    
    def findClusterPairs(self):  
        clusterPoints = []
        #create list of all gravityPoints
        for key in self.clusterGravityPointDictionary:
            clusterPoints.append( self.clusterGravityPointDictionary[key])
        
        #calculate distances between all points
        clustersDistanceMatrix = dist(np.array(clusterPoints))
        #search for pair
        for row in range(len(clustersDistanceMatrix)):
            minNumber = 99999
            minColmn = -1
            for colomn in range(len(clustersDistanceMatrix[row])):
                if clustersDistanceMatrix[row, colomn] == 0:
                    continue
                if clustersDistanceMatrix[row, colomn] < minNumber:
                    minNumber = clustersDistanceMatrix[row, colomn]
                    minColmn = colomn
            #add pair
            if (row in self.clusterPairsDictionary) == False:
                self.clusterPairsDictionary.update({row : minColmn })
                  
    
    #Calculate avg S values of the cluster
    def calculateAvgSilhoueteOfCluster(self, clusterNumber):     
        #because the calcualtion is the same for all the cluster member they will all have the same A value
        arrayAValues = self.calculateClusterAValue(clusterNumber)        
        arrayBValues = self.calculateBValues(clusterNumber)
        arraySValues =  np.zeros(len(self.clustersDictionaryIndexes[clusterNumber]))

        for i in range(len(arraySValues)):
            a = arrayAValues[i]
            b = arrayBValues[i]
            if a < b:
                arraySValues[i] = 1 - (a / b)
                continue
            if a == b:
                arraySValues[i] = 0
                continue
            arraySValues[i] = (b / a) - 1     
        return np.average(arraySValues)
        
    #calculation of A will be as followed:
    #a value will be the distance between pIndex to (gravityPoint - pIndex)
    def calculateClusterAValue(self, clusterNumber):
        #because all the memeber will have the same distance sum we can calculate it only once
        numberOfMembers = len(self.clustersDictionaryIndexes[clusterNumber])
        distancesList = []
        gravityCI = self.clusterGravityPointDictionary[clusterNumber]
        for i in range(numberOfMembers):
            distancesList.append(calcDistA(self.clustersDictionaryVectors[clusterNumber][i], gravityCI, numberOfMembers))
        
        
        return np.array(distancesList)
        
        

    #calculation of B will be as followed:
    #a value will be the distance between pIndex the closest gravityPoint CJ
    def calculateBValues(self, clusterNumber):   
        clusterCJ = self.clusterPairsDictionary[clusterNumber]
        amountOfCI = len(self.clustersDictionaryIndexes[clusterNumber])
        #amountOfMembersInCJ = len(self.clustersDictionaryVectors[clusterCJ])
        
        #current cluster points and cluster gravity point CJ
        listOfVectors = self.clustersDictionaryVectors[clusterNumber] + [self.clusterGravityPointDictionary[clusterCJ]]
        #calculate distances of all current points to the gravity point of the neighbor cluster
        distMatrix = dist(np.array(listOfVectors))
        #calculate sum of each row without there own members
        arrayOfDistancesSum = np.sum(distMatrix[0:amountOfCI, amountOfCI:],axis=1)
                               
        return arrayOfDistancesSum
        
                
        
    
def calcDistA(a, ac, size):
    if size == 1:
        return 0
    val = a - ((ac * size - a) / (size - 1))
    val2 = val * val
    sumOfAll = np.sum(val2)
    return (sumOfAll)**0.5

def dist(A):
    m, n = A.shape
    B = A @ A.T
    D = np.diag(B).reshape([1, m])
    return (D.T + D - 2 * B)**0.5