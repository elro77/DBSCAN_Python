import numpy as np
import time
import math

from sklearn.cluster import DBSCAN
from MyDBSCAN import CMyDBSCAN

"""
# this is very slow approach, it takes 10 seconds for 100 data
t = time.time()
with open("data.txt",'r') as f:
    lines = f.readlines()
    points = np.zeros([len(lines),len(lines[0].split(','))])
    for i in range(len(points)):
        point = [line[i].split(',') for line in lines]
        print("time: ",time.time() - t, i)
   
elapsed = time.time() - t
print(elapsed)
###
"""
"""
    Version 1.00
    for 2000 points -> optimal clustering 0.093 seconds
                       My clustering 521 seconds
"""

# this is a fast approach, it takes 4.5 seconds for reading and creating the whole dataset
# its work 223 times faster
t = time.time()
with open("data.txt",'r') as f:
    vectorsArray = [[float (i) for i in line.split(',')] for line in f.readlines()]
elapsed = time.time() - t
print("creating data time: ",elapsed)

testArray = vectorsArray[7000:10000]
#====== Sklearn =================
#the sklearn clustering takes 120 seconds to accomplish
#return an array where each index is the vector(point) and value is it clustering
#where -1 will represnt as a noise

t = time.time()
clustering = DBSCAN(eps=3, min_samples=2).fit(testArray)
labels = clustering.labels_
elapsed = time.time() - t
print("optimal clustering time: ",elapsed)

#=================================


#============ my implementation =============
t = time.time()
dbscan = CMyDBSCAN(len(testArray), 3, 2)
clusteringResult = dbscan.startClustering(testArray)
elapsed = time.time() - t
print("my clustering time: ",elapsed)

#=================================

"""
#check correctness
for i in range(len(labels)):
    if labels[i] != clusteringResult[i]:
        print("different at: ",i)
print("finish testing")

"""


#testing area

