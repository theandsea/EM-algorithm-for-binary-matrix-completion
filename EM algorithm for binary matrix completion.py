# input
import copy
import math


def EM_Update():
    # compute L
    L = 0

    # E-Step for Ru
    denominator = 0
    numerator = [None for i in range(4)]
    for t in range(len(rate)):  # t-people
        for i in range(4):  # i-,Z movie-goer type
            product = PZ[i]
            for j in range(len(rate[t])):  # j-,R movie
                if rate[t][j] == '1':
                    product *= PRZ[j][i]
                elif rate[t][j] == '0':
                    product *= (1 - PRZ[j][i])
            numerator[i] = product
        # get Ru
        sum = 0
        for i in range(4):
            sum += numerator[i]
        L += math.log(sum)
        for i in range(4):
            Ru[t][i] = numerator[i] / sum

    T = len(rate)
    L /= len(rate)
    # print(L)

    # M-Step for PZ, PRZ
    T = len(Ru)
    for i in range(4):
        sum = 0
        for t in range(T):
            sum += Ru[t][i]
        PZ[i] = sum / T

    for j in range(len(PRZ)):
        for i in range(4):
            sum = 0
            for t in range(T):
                if rate[t][j] == '1':
                    sum += Ru[t][i]
                elif rate[t][j] == '?':
                    sum += Ru[t][i] * PRZ[j][i]
            PRZ[j][i] = sum / (T * PZ[i])

    return L


from numpy import double

with open('hw8_ratings.txt') as file:
    line_s = file.readlines()
rate = [[] for i in range(len(line_s))]
for i in range(len(line_s)):
    line = line_s[i].replace("\n", "")
    numstr = line.split(" ")
    for j in range(len(numstr)):
        rate[i].append(numstr[j])

# print(rank)

popu = [None for j in range(len(rate[0]))]
for j in range(len(popu)):
    all = 0
    recom = 0
    for i in range(len(rate)):
        if rate[i][j] == '1':
            all += 1
            recom += 1
        elif rate[i][j] == '0':
            all += 1
    popu[j] = recom / all

with open('hw8_movies.txt') as file:
    line_s = file.readlines()
movie = [None for i in range(len(line_s))]
for i in range(len(line_s)):
    line = line_s[i].replace("\n", "")
    movie[i] = line
movie_origin=copy.deepcopy(movie)

for i in range(len(popu) - 1):
    for j in range(i, len(popu)):
        if popu[i] < popu[j]:
            popu[i], popu[j] = popu[j], popu[i]
            movie[i], movie[j] = movie[j], movie[i]

# print 1
""""""
print("=================overall ranking=====================")
print(len(popu))
for i in range(len(popu)):
    print(popu[i], "\t\t",movie[i])


# read PZ
PZ = [None for i in range(4)]
with open('hw8_probZ_init.txt') as file:
    line_s = file.readlines()
for i in range(len(line_s)):
    line = line_s[i].replace("\n", "")
    PZ[i] = double(line)

# read PRZ
with open('hw8_probR_init.txt') as file:
    line_s = file.readlines()
PRZ = [[None for i in range(4)] for j in range(len(line_s))]
for j in range(len(line_s)):
    line = line_s[j].replace("\n", "")
    numstr = line.split("   ")
    for i in range(4):
        PRZ[j][i] = double(numstr[i + 1])

# EM-algorithm
Ru = [[None for i in range(4)] for t in range(len(rate))]
""""""
print()
print()
print("=================EM-algorithm update=====================")
specific = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
now = 0
for times in range(256 + 2): #
    L = EM_Update()
    if times == specific[now]:
        print(times, "\t", L)
        now += 1


# recommend for my self
myindex=-1
id = [None for t in range(len(rate))]
with open('hw8_ids.txt ') as file:
    line_s = file.readlines()
for t in range(len(line_s)):
    line = line_s[t].replace("\n", "")
    id[t] = line
    if line=='A59013702':
        myindex=t

print()
print("====================my rate==================")
print(rate[myindex])

PRR_un=[] #None for j in range(len(movie_origin))
movie_un=[]
for j in range(len(movie_origin)):
    if rate[myindex][j]=='?':
        sum = 0
        for i in range(4):
            sum += Ru[myindex][i] * PRZ[j][i]
        PRR_un.append(sum)
        movie_un.append(movie_origin[j])

# ranking for my unseen movie
for j in range(len(PRR_un)-1):
    for i in range(j+1,len(PRR_un)):
        if PRR_un[j]<PRR_un[i]:
            PRR_un[j], PRR_un[i]=PRR_un[i],PRR_un[j]
            movie_un[j],movie_un[i]=movie_un[i],movie_un[j]

print()
print()
print("=================ranking recommendation for me=====================")
print(len(PRR_un))
for j in range(len(PRR_un)):
    print(PRR_un[j],"\t\t",movie_un[j])

