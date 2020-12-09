input_file = open("puzzle9.txt", "r")

n = []

num = 0

for i in input_file:
    n.append(int(i))

for i in range(25, len(n), 1):
    found = False
    for j in range(i-25, i, 1):
        for k in range(i-25, i, 1):
            if k==j:
                continue
            if n[j]+n[k] == n[i]:
                found = True
                break
        if found:
            break
    if not found:
        print(n[i])
        num = n[i]
        break

for i in range(0, len(n), 1):
    max_id = i
    count = n[i]
    n_min = n[i]
    n_max = n[i]
    while count<num:
        max_id +=1
        count += n[max_id]
        n_min = min(n_min, n[max_id])
        n_max = max(n_max, n[max_id])
    if count == num:
        print(n_min+n_max)
        break
