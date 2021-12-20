import numpy as np
import time
import math

from sklearn.cluster import DBSCAN
from MyDBSCAN import CMyDBSCAN
from silhouette import Silhouette

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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
    == Version 1.00, pure DBSCAN without any improvment
    for 2000 points -> optimal clustering 0.093 seconds
                       My clustering 521 seconds
                        Version 1.00
                        
    == Version 1.01, using a tile grid that will hold similliar vectors behavior and dictinaory to connect graph                   
    for 3000 points -> optimal clustering 0.287 seconds
                       My clustering 88 seconds
                       
    for 5000 points -> optimal clustering 0.605 seconds
                      My clustering 240 seconds
                      
                      
    == Version 1.02, improving the euqlidian distance function with np.array operations         
    for 3000 points -> optimal clustering 0.287 seconds
                       My clustering 16.4 seconds
                       
    for 5000 points -> optimal clustering 0.605 seconds
                      My clustering 44 seconds
                      
    for 10,000 points -> optimal clustering 2.72 seconds
                         My clustering 178 seconds
                         
                         
    == Version 1.03, using Dan's euclidean distance, saving the vectors for each grid group  
    for 3000 points -> optimal clustering 0.287 seconds
                       My clustering 1.87 seconds
                       
    for 5000 points -> optimal clustering 0.605 seconds
                      My clustering 5.2 seconds
                      
    for 10,000 points -> optimal clustering 2.72 seconds
                         My clustering 19.83 seconds
    for 50,000 points -> optimal clustering 32.14 seconds
                         My clustering very long time seconds  
                         
                         
    == Version 1.04, decreasing number pf iterations using group union                               
    for 5000 points -> optimal clustering 0.605 seconds
                      My clustering 0.93 seconds
                      
    for 10,000 points -> optimal clustering 2.72 seconds
                         My clustering 3.57 seconds
    for 50,000 points -> optimal clustering 32.14 seconds
                         My clustering 90.86 time seconds 
                         
                                            
     == Version 1.05, improving search by using a matrix and np.sum() for detecting 
                      how many points are connected to each other with eps distance
    for 5000 points -> optimal clustering 0.605 seconds
                      My clustering 0.198 seconds
                      
    for 10,000 points -> optimal clustering 2.72 seconds
                         My clustering 0.791 seconds
    for 50,000 points -> optimal clustering 32.14 seconds
                         My clustering 25.33 time seconds 
                         
   for 100,000 points -> optimal clustering 120 seconds
                         My clustering 135.77 time seconds 
                         
    == Version 1.06, after implementing silhouete i had to change eps to 4 and it broke dbscan so i had
                     to think for another way

    == Version 1.07, using matrixes and np.sum() np.where and running dbscan for each grid tile the results were improved for
    
                         
                         
    
                      
"""

# this is a fast approach, it takes 4.5 seconds for reading and creating the whole dataset
# its work 223 times faster
t = time.time()
with open("data.txt",'r') as f:
    vectorsArray = np.array([[float (i) for i in line.split(',')] for line in f.readlines()])
elapsed = time.time() - t
print("creating data time: ",elapsed)



testArray = vectorsArray[0:2000]
#====== Sklearn =================
#the sklearn clustering takes 120 seconds to accomplish
#return an array where each index is the vector(point) and value is it clustering
#where -1 will represnt as a noise

"""
t = time.time()
clustering = DBSCAN(eps=3, min_samples=2).fit(testArray)
labels = clustering.labels_
elapsed = time.time() - t
print("optimal clustering time: ",elapsed)

"""
#=================================


#============ my implementation =============
t = time.time()
dbscan = CMyDBSCAN(len(testArray), 4, 3)
myClusteringResult = dbscan.startClustering(testArray)
elapsed = time.time() - t
print("my clustering time: ",elapsed)

silhouette = Silhouette()

t = time.time()
silhouetteValue = silhouette.calculateSilhouetteValue(testArray, np.array(myClusteringResult))
elapsed = time.time() - t
print("calculateSilhouetteValue time: ",elapsed)


#=================================


#============ Plot =============
halfSize = int(len(testArray[0])/2)
xArray = np.average(testArray[: , 0 : halfSize], axis = 1)
yArray = np.average(testArray[: , halfSize+1 : len(testArray[0])], axis = 1)
colorsArray = {0 : mcolors.CSS4_COLORS['black'],
               1 : mcolors.CSS4_COLORS['darkorange'],
               2 : mcolors.CSS4_COLORS['lime'],
               3 : mcolors.CSS4_COLORS['red'],
               4 : mcolors.CSS4_COLORS['blue'],
               5 : mcolors.CSS4_COLORS['cyan'],
               6 : mcolors.CSS4_COLORS['darkviolet'],
               7 : mcolors.CSS4_COLORS['gold'],
               8 : mcolors.CSS4_COLORS['coral'],
               9 : mcolors.CSS4_COLORS['violet'],
               10 : mcolors.CSS4_COLORS['greenyellow'],
               11 : mcolors.CSS4_COLORS['dimgray'] 
            }

clusterColor = [colorsArray[i+1] for i in myClusteringResult]

plt.scatter(xArray, yArray, c = clusterColor)
plt.title('Silhouette = %1.3f' %silhouetteValue)
plt.xlabel('X')
plt.ylabel('Y')
plt.show()





#=================================


"""
#check correctness
for i in range(len(labels)):
    if labels[i] != myClusteringResult[i]:
        print("different at: ",i)
print("finish testing")

"""
#testing area

