#!/usr/bin/python3

import math


def get_row_number(seatCode, row):
    if seatCode[0] != "F" and seatCode[0] != "B":
        return row
    elif seatCode[0] == "B":
            row[0] = math.ceil((row[0] + row[1])/2)
    elif seatCode[0] == "F":
            row[1] = math.floor((row[0] + row[1])/2)
    get_row_number(seatCode[1:], row)
    return row


def get_column_number(seatCode, col):
    if not seatCode:
        return col
    if seatCode[0] == "R":
        col[0] = math.ceil((col[0] + col[1])/2)
    elif seatCode[0] == "L":
        col[1] = math.floor((col[0] + col[1])/2)
    get_column_number(seatCode[1:], col)
    return col


inputArray = []
with open("input_day5.txt") as inputFile:
    for row in inputFile:
        inputArray.append(row.strip())

SEATROWS = 127
SEATCOLUMNS = 7
CONSTANT = 8

higherSeatId = 0
seatsByRow = {}
for row in range(SEATROWS):
    seatsByRow[str(row)] = []

for seat in inputArray:
    row_number = get_row_number(seat, [0, SEATROWS])
    column_number = get_column_number(seat.replace("F", "").replace("B", ""), [0, SEATCOLUMNS])
    seatsByRow[str(row_number[0])].append(column_number[0])

for key in seatsByRow.keys():
    if int(key) > 0:
        if len(seatsByRow[key]) < 8 and len(seatsByRow[str(int(key)-1)]) > 0 and len(seatsByRow[str(int(key)+1)]) > 0:
            myRow = int(key)
            for col in range(8):
                if col not in seatsByRow[str(key)]:
                    myCol = col
                    break

print(myRow * CONSTANT + myCol)



