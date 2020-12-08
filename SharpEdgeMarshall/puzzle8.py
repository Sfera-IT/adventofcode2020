import re
import copy
input_file = open("puzzle8.txt", "r")

# STAR 1

cmds = []
idx = 0
acc = 0

for i in input_file:
    cmd = i.split()
    cmd.append(False)
    cmds.append(cmd)

while not cmds[idx][2]:
    print(cmds[idx])
    cmds[idx][2] = True

    if cmds[idx][0] == "nop":
        idx += 1
        continue
    elif cmds[idx][0] == "jmp":
        idx += int(cmds[idx][1])
        continue
    elif cmds[idx][0] == "acc":
        acc += int(cmds[idx][1])
        idx += 1
        continue

print(acc)

# STAR 2
input_file.seek(0)

cmds = []
idx = 0
acc = 0

for i in input_file:
    cmd = i.split()
    cmd.append(False)
    cmds.append(cmd)

for i in range(0,len(cmds),1):
    idx = 0
    acc = 0
    if cmds[i][0] == "acc":
        continue
    
    _cmds = copy.deepcopy(cmds)
    if _cmds[i][0] == "jmp":
        _cmds[i][0] = "nop"
    elif _cmds[i][0] == "nop":
        _cmds[i][0] = "jmp"
    while not _cmds[idx][2] and idx != len(_cmds)-1:
        _cmds[idx][2] = True

        if _cmds[idx][0] == "nop":
            idx += 1
            continue
        elif _cmds[idx][0] == "jmp":
            idx += int(_cmds[idx][1])
            continue
        elif _cmds[idx][0] == "acc":
            acc += int(_cmds[idx][1])
            idx += 1
            continue

    if idx == len(_cmds)-1:
        break

print(acc)