import numpy as np
import math

class CMyDBSCAN:
    def __init__(self, _size, _eps ,_minPoints):
        #arrays
        self.clusters = [-1] * _size
        #sets
        self.noisePoints = {}
        self.remainingPoints = {i for i in range(_size)}
        #integers
        self.minPoints = _minPoints
        self.eps = _eps
        self.currnetCluster = 0
        
    def startClustering(self, dataSet):
        return self.clusters



    

def rangeQuery(data, point, eps):
    return 0
    
    
def calcEuclideanDistance(p1 ,p2):
    sm = 0
    for i in range(len(p1)):
        sm = sm + (p1[i]-p2[i]) * (p1[i]-p2[i])
    return math.sqrt(sm)
    