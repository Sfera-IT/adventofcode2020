#!/usr/bin/python3

instructions = []
with open('input_day8.txt') as inputFile:
    for instruction in inputFile:
        instructions.append(instruction.strip())

print (instructions)
acc = 0
executed_instructions = []
iterator = 0
prevIterator = 0

while True:
    instruction = instructions[iterator]
    if iterator in executed_instructions:
        print("iterator {} found in {}".format(iterator,executed_instructions))
        break
    else:
        operation = instruction.strip().split(" ")[0]
        argument = int(instruction.strip().split(" ")[1])
        executed_instructions.append(iterator)
        if operation == "jmp":
            print("hitting jmp, argument {}, iterator {}".format(argument,iterator))
            prevIterator = iterator
            iterator += argument
        elif operation == "acc":
            print("hitting acc, argument {}, iterator {}".format(argument, iterator))
            prevIterator = iterator
            iterator += 1
            acc += argument
        elif operation == "nop":
            print("hitting jmp, argument {}, iterator {}".format(argument, iterator))
            prevIterator = iterator
            iterator += 1


print(acc)
print(prevIterator)
