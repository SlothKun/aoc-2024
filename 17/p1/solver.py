#!/usr/bin/env python3
import time

# https://tschinz.github.io/days-of-algo/content/notebooks/010-maze-solver-dijkstra.html
# https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Related_problems_and_algorithms

def getTime(start_time):
    elapsed_time = time.time() - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    milliseconds = (seconds - int(seconds)) * 1000
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{int(milliseconds):03}"

start_time = time.time()
total = 0

# opc -> value to be read
# Operand -> code next to OPC
# Literal Operand (LO) = Value of the operand itself
# Combo Operand (CO) -
# 0 to 3 -> Is the value 0 to 3
# 4 -> Value of R-A
# 5 -> Value of R-B
# 6 -> Value of R-C
# 7 -> Reserved (should not appear)
#
#Instructions :
# 0 - adv
#   division R-A by 2^CO -> Truncate result into Int -> Write to A
# 1 - bxl
#   bitwise XOR between R-B and LO -> R-b
# 2 - bst
#   CO % 8 -> R-B
# 3 - jnz
#   Do nothing if R-A = 0
#   Else : Jump to LO (dont icrease LO by 2)
# 4 - bxc
#   bitWise XOR between R-B and R-C -> R-B
# 5 - out
#   CO % 8 -> Print (sep by comma) (store in str)
# 6 - bdv
#   division R-A by 2^CO -> Truncate result into Int -> Write to B
# 7 - cdv
#   division R-A by 2^CO -> Truncate result into Int -> Write to C

register = []
prog = []
insPo = 0
output = ""

with open("../input",'r') as ofile:
    lIdx = 0
    for line in ofile.readlines():
        if lIdx in [0,1,2]:
            register.append(int(line.split(" ")[2]))
        elif lIdx == 4:
            prog = [int(i) for i in line.split(" ")[1].split(',')]
        lIdx+=1


def getComboOp(lo, register):
    if lo in [0,1,2,3]:
        return lo
    elif lo == 4:
        return register[0]
    elif lo == 5:
        return register[1]
    elif lo == 6:
        return register[2]
    else:
        print(f"ERROR : lo == {lo}")

def applyInstruct(opc, lo, insPo, co, register, output):
    jmp = False
    if opc == 0:
        print("Instruction : adv")
        register[0] = register[0] // (2 ** co)
    elif opc == 1:
        print("Instruction : bxl")
        register[1] = register[1] ^ lo
    elif opc == 2:
        print("Instruction : bst")
        register[1] = co % 8
    elif opc == 3:
        if register[0] != 0:
            print("Instruction : jnz")
            jmp = True
        else:
            print("Instruction : None")
    elif opc == 4:
        print("Instruction : bxc")
        register[1] = register[1] ^ register[2]
    elif opc == 5:
        print("Instruction : out")
        output += f",{co%8}"
    elif opc == 6:
        print("Instruction : bdv")
        register[1] = register[0] // (2 ** co)
    elif opc == 7:
        print("Instruction : cdv")
        register[2] = register[0] // (2 ** co)

    insPo = insPo+2 if not jmp else lo
    return insPo, co, register, output


print(f"Register at load : {register}")
print(f"Prog at load : {prog}\n")

while insPo < len(prog):
    opc = prog[insPo]
    lo = prog[insPo+1]
    co = getComboOp(lo, register)
    print(f"--- loIDX = {insPo} | opc = {opc} | lo = {lo} | co = {co} ---")
    insPo, co, register, output = applyInstruct(opc, lo, insPo, co, register, output)
    print(f"Register after instruction : {register}")
    print(f"insPo after instruct : {insPo}")


print(f"\nRegister after instr : {register}")
print(f"Output after instr : {output[1:]}\n")
print(f"Answer : {output[1:]} - Program took : {getTime(start_time)} to run.")
