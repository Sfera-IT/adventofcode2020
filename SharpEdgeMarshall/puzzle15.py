import copy

with open('puzzle15.txt', 'r') as input_file:
    trn = list(map(int,input_file.readline()[:-1].split(",")))


# STAR 1
for idx in range(len(trn), 2020):
    occ = [i for i, e in enumerate(trn) if e == trn[idx-1]]
    occ.reverse()
    if occ == [idx-1]:
        trn.append(0)
    else:
        trn.append(occ[0] - occ[1])
    print(trn[idx])
print(trn[2019])
import copy

dic = {}

with open('puzzle15.txt', 'r') as input_file:
    trn = list(map(int,input_file.readline()[:-1].split(",")))


# STAR 1
for idx in range(len(trn), 2020):
    occ = [i for i, e in enumerate(trn) if e == trn[idx-1]]
    occ.reverse()
    if occ == [idx-1]:
        trn.append(0)
    else:
        trn.append(occ[0] - occ[1])
print(trn[2019])

# STAR 2
with open('puzzle15.txt', 'r') as input_file:
    trn = list(map(int,input_file.readline()[:-1].split(",")))
    for num in trn:
        dic[num] = [trn.index(num), None]

def run_turn(idx, num):
    val = num
    if num in dic:
        dic[num][1] = dic[num][0]
        dic[num][0] = idx
    else:
        dic[num] = [idx, None]
    return val

num = trn[len(trn)-1]

for idx in range(len(trn), 30000000):
    if num in dic and dic[num][1] != None:
        num = run_turn(idx, dic[num][0]-dic[num][1])     
    else:
        num = run_turn(idx, 0)
print(num)


# STAR 2
for idx in range(len(trn), 30000000):
    occ = [i for i, e in enumerate(trn) if e == trn[idx-1]]
    occ.reverse()
    if occ == [idx-1]:
        trn.append(0)
    else:
        trn.append(occ[0] - occ[1])
    print(trn[idx])
print(trn[30000000-1])
