import numpy as np
import time

from sklearn.cluster import DBSCAN

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


# this is a fast approach, it takes 4.5 seconds for reading and creating the whole dataset
# its work 223 times faster
t = time.time()
with open("data.txt",'r') as f:
    vectorsArray = np.array([[float (i) for i in line.split(',')] for line in f.readlines()])
elapsed = time.time() - t
print("creating data time: ",elapsed)

#the sklearn clustering takes 120 seconds to accomplish
#return an array where each index is the vector(point) and value is it clustering
#where -1 will represnt as a noise
"""
t = time.time()
clustering = DBSCAN(eps=3, min_samples=2).fit(vectorsArray)
elapsed = time.time() - t
print("clustering time: ",elapsed)
"""
#my implementation








