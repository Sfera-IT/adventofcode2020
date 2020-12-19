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
