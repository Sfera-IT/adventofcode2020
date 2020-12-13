import math

input_file = open("puzzle12.txt", "r")

# STAR 1

dirs = ["E","S","W","N"]

cmds = []
spos = [0,0]
sdir = 0

for i in input_file:
    cmds.append((i[0:1], int(i[1:-1])))

def move(mdir, mlen):
    if mdir == "E":
        spos[0] += mlen
    elif mdir == "W":
        spos[0] += -mlen
    elif mdir == "N":
        spos[1] += -mlen
    elif mdir == "S":
        spos[1] += mlen

for cmd in cmds:
    if cmd[0] in ["L", "R"]:
        sdir += cmd[1] if cmd[0] == "R" else -cmd[1]
    elif cmd[0] == "F":
        res_dir = sdir//90 % 4
        move(dirs[res_dir], cmd[1])
    else:
        move(cmd[0],cmd[1])

print(abs(spos[0])+abs(spos[1]))

# STAR 2

spos = [0,0]
wpos = [10,-1]

def movewp(mdir, mlen):
    if mdir == "E":
        wpos[0] += mlen
    elif mdir == "W":
        wpos[0] += -mlen
    elif mdir == "N":
        wpos[1] += -mlen
    elif mdir == "S":
        wpos[1] += mlen

def rotatewp(angle):
    s = math.sin(math.radians(angle))
    c = math.cos(math.radians(angle))
    newx = wpos[0]*c - wpos[1]*s
    newy = wpos[0]*s + wpos[1]*c
    wpos[0] = newx
    wpos[1] = newy

for cmd in cmds:
    if cmd[0] in ["L", "R"]:
        rotatewp(cmd[1] if cmd[0] == "R" else -cmd[1])
    elif cmd[0] == "F":
        spos[0] += wpos[0]*cmd[1]
        spos[1] += wpos[1]*cmd[1]
    else:
        movewp(cmd[0],cmd[1])

print(abs(spos[0])+abs(spos[1]))