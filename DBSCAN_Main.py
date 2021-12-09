import numpy as np
import time

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
# this is a fast approach, it takes 3.8 seconds for reading and creating the whole dataset
# its work 2631 times faster
t = time.time()
with open("data.txt",'r') as f:
    vectorsList = [[float (i) for i in line.split(',')] for line in f.readlines()]
elapsed = time.time() - t
print(elapsed)

