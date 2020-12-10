with open('puzzle10.txt','r') as f:
    data = f.read()[:-1].split('\n')

adp = sorted(list(map(int, data)))
adp.insert(0,0)

# STAR 1
c_1=0
c_3=1

for i in range(len(adp)):
    if i == 0:
        continue
    if adp[i] - adp[i-1] == 1:
        c_1 += 1
    elif adp[i] - adp[i-1] == 3:
        c_3 += 1

print(c_1*c_3)

# STAR 2

adp.append(adp[-1]+3)

adpm = dict.fromkeys(adp, 0)

for i in reversed(range(len(adp))):
    if i == len(adp)-1:
        adpm[adp[i]] = 1
        continue
    for j in range(i+1,min(len(adp),i+4)):
        if adp[j] > adp[i] + 3:
                break
        adpm[adp[i]] += adpm[adp[j]]

print(adpm)
