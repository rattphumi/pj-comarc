"""
Behavioral simulator สำหรับเครื่อง SMC (8 registers, 32-bit, 65536 words)

วิธีใช้:  python simulator.py <machine-code-file>

"""

import sys

NUMMEMORY = 65536   # จำนวน word ของ memory
NUMREGS = 8         # จำนวน register


class State:
    def __init__(self):
        self.pc = 0                     # address ของคำสั่งที่กำลังจะทำ
        self.mem = [0] * NUMMEMORY      # memory ทุกช่องเริ่มเป็น 0
        self.reg = [0] * NUMREGS        # register ทุกตัวเริ่มเป็น 0
        self.numMemory = 0              # จำนวนบรรทัดในไฟล์ machine code


def printState(state):
    print("\n@@@\nstate:")
    print("\tpc %d" % state.pc)
    print("\tmemory:")
    for i in range(state.numMemory):
        print("\t\tmem[ %d ] %d" % (i, state.mem[i]))
    print("\tregisters:")
    for i in range(NUMREGS):
        print("\t\treg[ %d ] %d" % (i, state.reg[i]))
    print("end state")


def loadProgram(state, fileName):
    try:
        f = open(fileName, "r")
    except OSError as e:
        print("error: can't open file %s" % fileName)
        print("fopen: %s" % e.strerror)
        sys.exit(1)

    with f:
        for line in f:
            try:
                value = int(line) #แปลงข้อความเป็นตัวเลข
            except ValueError:  #ถ้าไม่ใช่ตัวเลข
                print("error in reading address %d" % state.numMemory)
                sys.exit(1)
            if state.numMemory >= NUMMEMORY: #ตรวจว่า mem ยังไม่เต็ม
                print("error: program too large for memory")
                sys.exit(1)

            state.mem[state.numMemory] = value
            print("memory[%d]=%d" % (state.numMemory, value))
            state.numMemory += 1


def convertNum(num):
    """ แปลงเลข 16 bit sign extension ใช้เเก้ lw, sw และ beq """
    if num & (1 << 15):          
        num -= (1 << 16)
    return num


def toInt32(num):
    """ บีบค่าให้อยู่ในช่วง 32-bit signed เพราะ Python ไม่มีขีดจำกัด """
    num = num & 0xFFFFFFFF    #num จะเป็นเท่าไหร่ก็ตามเเต่จะ limit เเค่ 32 bit โดยนำไป & 0xFFFFFFFF คือ 1 จำนวน 32 ตัว
    if num & (1 << 31):          
        num -= (1 << 32)         
    return num


def checkAddress(addr):
    """ตรวจว่า address ของ lw/sw อยู่ใน memory (0 ถึง 65535)"""
    if addr < 0 or addr >= NUMMEMORY:
        print("error: memory address out of range (%d)" % addr)
        sys.exit(1)


def execute(state, instr):
    #decode
    opcode  = (instr >> 22) & 0x7              # bits 24-22
    regA    = (instr >> 19) & 0x7              # bits 21-19
    regB    = (instr >> 16) & 0x7              # bits 18-16
    destReg = instr & 0x7                      # bits 2-0   (R-type)
    offset  = convertNum(instr & 0xFFFF)       # bits 15-0  (I-type)

    reg = state.reg
    nextPC = state.pc + 1                 
    halted = False

    #execute
    if opcode == 0:   # add
        reg[destReg] = toInt32(reg[regA] + reg[regB])

    elif opcode == 1:   # nand (bitwise)
        reg[destReg] = toInt32(~(reg[regA] & reg[regB]))

    elif opcode == 2:    # lw:regB = mem[regA + offset]
        addr = reg[regA] + offset
        checkAddress(addr)
        reg[regB] = state.mem[addr]

    elif opcode == 3:    # sw:mem[regA + offset] = regB
        addr = reg[regA] + offset
        checkAddress(addr)
        state.mem[addr] = reg[regB]

    elif opcode == 4:    # beq:ถ้าเท่ากัน ไป PC+1+offset
        if reg[regA] == reg[regB]:
            nextPC = state.pc + 1 + offset

    elif opcode == 5:     # jalr
        reg[regB] = state.pc + 1
        nextPC = reg[regA]

    elif opcode == 6:     # halt:เพิ่ม PC ตามปกติ แล้วหยุด
        halted = True
    state.pc = nextPC
    return halted


def run(state):
    instrCount = 0

    while True:
        printState(state)                     

        # กัน pc หลุดออกนอก memory (เช่นกระโดดไป address -1)
        if state.pc < 0 or state.pc >= NUMMEMORY:
            print("error: pc out of range (%d)" % state.pc)
            sys.exit(1)

        instr = state.mem[state.pc]           # fetch
        instrCount += 1                       # นับทุกคำสั่ง รวม halt ด้วย
        halted = execute(state, instr)        # decode + execute

        if halted:
            break

    print("machine halted")
    print("total of %d instructions executed" % instrCount)
    print("final state of machine:")
    printState(state)                      


def main():
    if len(sys.argv) != 2:
        print("error: usage: %s <machine-code file>" % sys.argv[0])
        sys.exit(1)

    state = State()                           
    loadProgram(state, sys.argv[1])
    print()                                   
    run(state)
    sys.exit(0)


if __name__ == "__main__":
    main()