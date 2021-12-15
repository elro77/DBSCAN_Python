import numpy as np
import math
import time
import random

class CBallTree:
    def __init__(self):
        self.root = None
        self.connectionDictionary = dict()
     
    def constructTree(self, data):
        if len(data) == 1:
            self.root = CNode(data[0], None, None)
            return self.root
        
        t = time.time()
        startIndex = random.randint(0, len(data))
        firstFarest = searchForFarestPoint(data, startIndex)
        secondFarest = searchForFarestPoint(data, firstFarest)
        
        elapsed = time.time() - t
        print("finding farest points time: ",elapsed)
        
        
        
        
        
        return self.root
    
    def searchNeighbors(self, data):
        x=0

def searchForFarestPoint(data, pIndex):
    minDistance = 0
    foundIndex = 0
    for qIndex in range(len(data)):
        calcDist = calcEuclideanDistance(data, qIndex ,pIndex)
        if  calcDist > minDistance:
            calcDist = minDistance
            foundIndex = qIndex
    return foundIndex


        
def calcEuclideanDistance(data, qIndex ,pIndex):
        sm = 0
        p1 = data[qIndex]
        p2 = data[pIndex]
        for i in range(len(p1)):
            sm += (p1[i]-p2[i]) * (p1[i]-p2[i])
        return math.sqrt(sm)       
class CNode:
    def __init__(self, _point, _left, _right):
        self.median = _point
        self.leftTree = _left
        self.rightTree = _right
        self.pointsIndexesArray = []