import numpy as np
import math


def myDBSCAN(data, minPoints, eps):
    return 0
    
    
    

def rangeQuery(data, point, eps):
    return 0
    
    
def calcEuclideanDistance(p1 ,p2):
    sm = 0
    for i in range(len(p1)):
        sm = sm + (p1[i]-p2[i]) * (p1[i]-p2[i])
    return math.sqrt(sm)
    