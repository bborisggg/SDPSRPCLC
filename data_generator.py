import pandas as pd
from random import randint, choice, sample
import scipy.stats as stats
import numpy as np


# Parameters
K = 10
N = 25
print(N, 12*60, K)
# Generate list of coordinates
# Depo is located at (0,0)
# Stations are located from (100,100) to (200,200)
# Distances are normalized so that t((0,0),(200,200)) = 120, 
coord = [(0,0)]
for _ in range(N-1):
    coord.append((100+randint(0,100), 100+randint(0,100)))
# Distances matrix
cnt = 0
for i in range(N):
    for j in range(N):
        if i==j:
            print(0, end=" ")
        elif i==0 or j==0:
            print(int((abs(coord[i][0]-coord[j][0]) + abs(coord[i][1]-coord[j][1]))*60//200), end=" ")
        else:
            thr = sorted([int((abs(coord[i][0]-coord[k][0]) + abs(coord[i][1]-coord[k][1]))*60//200) for k in range(N) if k!= i])[N//4]
            if (int((abs(coord[i][0]-coord[j][0]) + abs(coord[i][1]-coord[j][1]))*60//200) > thr):
                print(13*60, end=' ')
            else:
                print(int((abs(coord[i][0]-coord[j][0]) + abs(coord[i][1]-coord[j][1]))*60//200), end=" ")
    print('')
# order
lst = []
desc = [] # (is_left, is_right), is_heavy
for i in range(N):
    if i == 0:
        lst.append([])
        desc.append(((True, True),True))
    else:
        # choose
        f = (True, True)
        p = randint(0,9)
        if p <= 2:
            f = (False, True)
        elif p >= 7:
            f = (True, False)
        desc.append((f,randint(0,9)<=2))
        num = stats.poisson.rvs(4.2, size=1)[0]
        l = []
        for i in range(num):
            capacity = np.exp(stats.norm.rvs(loc=10, scale=0.4, size=1))[0]
            occupancy = stats.beta.rvs(a=4.5,b=1.4,size=1)[0]
            if (occupancy < 0.6):
                l.append((int(0.6*capacity),int(0.98*capacity)))
        lst.append(l)
for el in lst:
    print(len(el), end=' ')
    for l in el:
        print(l[0], end=' ')
    print()
print()
for el in lst:
    print(len(el), end=' ')
    for l in el:
        print(l[1], end=' ')
    print()
print()

desc_trucks = []
for i in range(K):
    num = 5
    r = randint(0,9)
    if r <= 2:
        num = 4
    elif r >= 7:
        num = 6
    print(num, end= " ")
    sm = 0
    for _ in range(num):
        c = int(np.exp(stats.norm.rvs(loc=9, scale=0.3, size=1))[0])
        sm += c
        print(c, end= " ")
    print()
    f = (True, True)
    p = randint(0,9)
    if p <= 2:
        f = (False, True)
    elif p >= 7:
        f = (True, False)
    desc_trucks.append((f,sm))
# Service times
for i in range(K):
    print(int(desc_trucks[i][1]//1000*3), end=' ')
print()
for k in range(K):
    for i in range(N):
        ok = ((desc[i][0][0] and desc_trucks[k][0][0]) or (desc[i][0][1] and desc_trucks[k][0][1])) and \
             ((desc[k][1]<40000) or (desc_trucks[k][1] > 40000) and desc[i][1])
        print(int(ok), end = ' ')
    print('')

