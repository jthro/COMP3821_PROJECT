import random


random_arrays = [[]]
from itertools import combinations_with_replacement

perms = list(combinations_with_replacement([1,2,3], 4))
perms2 = list(combinations_with_replacement([1,2,3], 4))
print(len(perms))
# perms = [[1,1,1,1]]
# perms2 = [[3,3,3,3]]


countAll = 0
countLosses = 0
countGains = 0

expected1 = 0
expected2 = 0

for i in perms:
    for j in perms2:
        P1 = (4 - i.count(1)) / ((3 - 1) * 4)
        P2 = (4 - i.count(2)) / ((3 - 1) * 4)
        P3 = (4 - i.count(3)) / ((3 - 1) * 4)

        P = [0, P1, P2, P3]

        ## i[0]
        vertexArray = [[1,3,0], [0, 2, 1], [1, 3, 2], [0, 2, 3]]

        # 0--1
        # |  |
        # 3--2

    
        neutralO = 0
        positiveO = 0
        negativeO = 0

        neutral = 0
        positive = 0
        negative = 0


        for f in vertexArray:
            array1 = [i[f[0]], i[f[1]]]
            array2 = [j[f[0]], j[f[1]]]
            

            
            for k in range(1,4): 
                if (k in array1 == k in array2): 
                    neutralO += P[k] *1/4
                    neutral += 1/3 *1/4
                elif (k in array1 or k in array2): 
                    if ((i[f[2]] == k and (not k in array2))or (j[f[2]] == k and (not k in array1))):
                        positiveO += P[k] *1/4
                        positive +=  1/3 *1/4
                        continue
                    negativeO += P[k] *1/4
                    negative += 1/3 *1/4



                else: 
                    # If the two graphs have the same current vertex
                    if (i[f[2]] == j[f[2]] and i[f[2]] == k): 
                        neutralO += P[k] *1/4
                        neutral += 1/3 *1/4
                        continue
                    positiveO += P[k] *1/4
                    positive +=  1/3 *1/4


        expectedO = positiveO * -1 + negativeO * 1
        expected = positive * -1 + negative * 1
        countAll = countAll +1
        if (expected < expectedO):
            print(i,j, expected, expectedO) 
            countLosses = countLosses +1
        if (expected > expectedO):
            countGains = countGains +1
        expected1 += expected
        expected2 += expectedO


print("Losses", countLosses/ countAll)
print("Gains", countGains/ countAll)
print("Countall", countAll)
print("Expected Normally", expected1 / countAll)
print("Expected Ours", expected2 / countAll)









