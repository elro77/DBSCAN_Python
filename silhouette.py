import numpy as  np
import math
import time


"""
t = time.time()
elapsed = time.time() - t
print("creating graph time: ",elapsed)
"""

clustersDictionary = dict()
arrayValueA = np.zeros()
arrayValueB = np.zeros()

def calculateSilhouetteValue(dataset, clusters):
    x=0
    
    
def createClustersDictionary(clusters):
    x=0

def calculateValueA(cluster):
    x=0
    
def calculateValueB(cluster):
    x=0

def calculateAvgSilhouete():
    x=0


def dist(A):
    m, n = A.shape
    B = A @ A.T
    D = np.diag(B).reshape([1, m])
    return (D.T + D - 2 * B)**0.5