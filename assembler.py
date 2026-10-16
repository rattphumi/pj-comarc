import sys #ใช้อ่านไฟล์และพิมพ์ข้อความ error
import re #ใช้ตรวจสอบ Label ของคำสั่ง

# set ของคำสั่งทั้งหมด
VALID_OPCODES = {'add', 'nand', 'lw', 'sw', 'beq', 'jalr', 'halt', 'noop', '.fill'}
# เลข opcode ของแต่ละคำสั่ง
OPCODE_MAP = {
    'add':  0b000,
    'nand': 0b001,
    'lw':   0b010,
    'sw':   0b011,
    'beq':  0b100,
    'jalr': 0b101,
    'halt': 0b110,
    'noop': 0b111
}

# ใช้ตรวจสอบ Label ตัวแรกต้องขึ้นต้นด้วยตัวอักษรและตามด้วยตัวอักษรหรือตัวเลข 
LABEL_PATTERN = re.compile(r'^[A-Za-z][A-Za-z0-9]*$') # ยาวไม่เกิน 6 ตัวอักษร

# แสดงข้อความ error ไปที่ stderr และยุติการทำงานด้วย exit(1) 
def exit_with_error(msg):
    sys.stderr.write(f"Error: {msg}\n")
    sys.exit(1)

# ตรวจสอบว่าเป็น integer ไหม
def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# ตรวจสอบว่า register เป็น integer และอยู่ในช่วง 0-7 และคืนค่า register เป็น integer หากไม่ถูกต้องจะ exit_with_error 
def check_register(reg_str, line_num):
    if not is_integer(reg_str):
        exit_with_error(f"Line {line_num}: Register '{reg_str}' is not an integer")
    reg = int(reg_str)
    if reg < 0 or reg > 7: 
        exit_with_error(f"Line {line_num}: Register '{reg}' is out of range 0-7")
    return reg

# ตรวจสอบว่า offset เป็น integer และอยู่ในช่วง -32768 ถึง 32767 และคืนค่า offset เป็น integer หากไม่ถูกต้องจะ exit_with_error เพราะ offset ของ lw, sw, beq ต้องเป็น 16-bit signed integer
def check_offset_16bit(val, line_num):
    if val < -32768 or val > 32767:
        exit_with_error(f"Line {line_num}: Offset {val} exceeds 16-bit signed limit (-32768 to 32767)")
    return val & 0xFFFF # คืนค่า offset เป็น 16-bit unsigned integer (ใช้ & 0xFFFF) เพื่อให้สามารถเก็บค่าใน machine code ได้

# ตรวจสอบว่า .fill value เป็น integer และอยู่ในช่วง -2147483648 ถึง 2147483647 และคืนค่าเป็น integer หากไม่ถูกต้องจะ exit_with_error เพราะ .fill ต้องเป็น 32-bit signed integer
def check_fill_32bit(val, line_num):
    if val < -2147483648 or val > 2147483647:
        exit_with_error(f"Line {line_num}: .fill value {val} exceeds 32 bits")
    return val # คืนค่าเป็น integer เพราะ .fill สามารถเก็บค่า 32-bit signed integer ได้

# จำนวน Instruction field ที่แต่ละ opcode ต้องการ เกินจากนี้ถือเป็น Comment
FIELD_COUNT = {
    'add': 3, 'nand': 3, 'lw': 3, 'sw': 3, 'beq': 3,
    'jalr': 2, 'halt': 0, 'noop': 0, '.fill': 1
}

# แยกบรรทัดเป็น label, opcode, fields, comment 
def parse_line(raw_line, line_num):

    # ลบ newline(\n) และ carriage return(\r) ออกจากท้ายบรรทัด 
    line = raw_line.rstrip('\r\n') 
    if not line.strip():
        return None

    # แยก label, opcode, fields, comment
    tokens = line.split()
    label = None
    if line[0] not in (' ', '\t'): 
        label = tokens[0]
        tokens = tokens[1:] 

    if not tokens:
        exit_with_error(f"Line {line_num}: Missing opcode after label")

    # ตรวจสอบว่า opcode เป็นคำสั่งที่มีอยู่ใน VALID_OPCODES และตรวจสอบจำนวน fields ที่ต้องการ
    opcode = tokens[0]
    if opcode not in VALID_OPCODES:
        exit_with_error(f"Line {line_num}: Unrecognized opcode '{opcode}'")

    need = FIELD_COUNT[opcode]
    rest = tokens[1:] 
    if len(rest) < need: 
        exit_with_error(f"Line {line_num}: {opcode} requires {need} fields")

    fields = rest[:need] 
    comment = ' '.join(rest[need:]) # รวม comment ที่เหลือหลัง fields เป็น string เดียว
    return label, opcode, fields, comment

def assemble(input_filename, output_filename): 
    # อ่านไฟล์ input และเก็บบรรทัดทั้งหมดใน lines
    try:
        with open(input_filename, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
    except FileNotFoundError:
        exit_with_error(f"Cannot open input file '{input_filename}'")

    symbol_table = {}
    parsed_instructions = []
    address = 0
    for line_num, raw_line in enumerate(lines, start=1): 
        parsed = parse_line(raw_line, line_num)
        if parsed is None:
            continue  # ข้ามบรรทัดว่าง
        label, opcode, args, comment = parsed
        # ตรวจว่า label ไม่ซ้ำกันและเก็บลงใน symbol_table
        if label is not None:
            if len(label) > 6:
                exit_with_error(f"Line {line_num}: Label '{label}' exceeds 6 characters")
            if not LABEL_PATTERN.match(label): 
                exit_with_error(f"Line {line_num}: Invalid label '{label}' (must begin with a letter and contain only alphanumeric characters)")
            if label in symbol_table: 
                exit_with_error(f"Line {line_num}: Duplicate label '{label}'")
            symbol_table[label] = address

        parsed_instructions.append((address, opcode, args, line_num)) 
        address += 1

    machine_codes = []
    # แปลงคำสั่งเป็น machine code
    for pc, opcode, args, line_num in parsed_instructions: 
        if opcode == '.fill': # ตรวจสอบว่า .fill มี argument เป็น integer หรือ label ที่มีอยู่ใน symbol_table ถ้ามีให้ใช้ค่าของ label นั้น
            if len(args) < 1:
                exit_with_error(f"Line {line_num}: .fill missing argument")
            arg = args[0]
            if is_integer(arg):
                val = check_fill_32bit(int(arg), line_num)
            else:
                if arg not in symbol_table:
                    exit_with_error(f"Line {line_num}: Undefined label '{arg}' in .fill")
                val = symbol_table[arg] 
            machine_codes.append(val)
    
        elif opcode in ['add', 'nand']: # ตรวจสอบว่า add, nand มี argument เป็น register ทั้งหมด 3 ตัว 
            if len(args) < 3:
                exit_with_error(f"Line {line_num}: {opcode} requires 3 fields")
            reg_a = check_register(args[0], line_num)
            reg_b = check_register(args[1], line_num)
            dest_reg = check_register(args[2], line_num)
            code = (OPCODE_MAP[opcode] << 22) | (reg_a << 19) | (reg_b << 16) | dest_reg 
            machine_codes.append(code) 

        elif opcode in ['lw', 'sw']: # ตรวจสอบว่า lw, sw มี argument เป็น register 2 ตัว และ offset เป็น integer หรือ label 
            if len(args) < 3:
                exit_with_error(f"Line {line_num}: {opcode} requires 3 fields")
            reg_a = check_register(args[0], line_num)
            reg_b = check_register(args[1], line_num)
            offset_field = args[2]
            if is_integer(offset_field):
                offset = int(offset_field)
            else:
                if offset_field not in symbol_table:
                    exit_with_error(f"Line {line_num}: Undefined label '{offset_field}'")
                offset = symbol_table[offset_field]
            code = (OPCODE_MAP[opcode] << 22) | (reg_a << 19) | (reg_b << 16) | check_offset_16bit(offset, line_num) # ตรวจสอบว่า offset อยู่ในขอบเขต 16 บิต
            machine_codes.append(code)

        elif opcode == 'beq': # ตรวจสอบว่า beq มี argument เป็น register 2 ตัว และ offset เป็น integer หรือ label
            if len(args) < 3:
                exit_with_error(f"Line {line_num}: beq requires 3 fields")
            reg_a = check_register(args[0], line_num)
            reg_b = check_register(args[1], line_num)
            offset_field = args[2]
            if is_integer(offset_field):
                offset = int(offset_field)
            else:
                if offset_field not in symbol_table:
                    exit_with_error(f"Line {line_num}: Undefined label '{offset_field}'")
                offset = symbol_table[offset_field] - (pc + 1) # คำนวณ offset เป็น PC + 1 + offset
            code = (OPCODE_MAP[opcode] << 22) | (reg_a << 19) | (reg_b << 16) | check_offset_16bit(offset, line_num)
            machine_codes.append(code)

        elif opcode == 'jalr': # ตรวจสอบว่า jalr มี argument เป็น register 2 ตัว
            if len(args) < 2:
                exit_with_error(f"Line {line_num}: jalr requires 2 fields")
            reg_a = check_register(args[0], line_num)
            reg_b = check_register(args[1], line_num)
            code = (OPCODE_MAP[opcode] << 22) | (reg_a << 19) | (reg_b << 16)
            machine_codes.append(code)

        elif opcode in ['halt', 'noop']: # ไม่จำเป็นต้องตรวจ argument เพราะ halt และ noop ไม่มี argument
            code = (OPCODE_MAP[opcode] << 22) # field ที่ไม่ถูกใช้จะเป็น comment 
            machine_codes.append(code)

    # เขียน machine code ลงไฟล์ output
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for code in machine_codes:
                f.write(f"{code}\n")
    except Exception as e:
        exit_with_error(f"Cannot write output file: {e}")

    print(f"created '{output_filename}'")
    sys.exit(0)

if __name__ == '__main__': 
    if len(sys.argv) != 3:
        exit_with_error("Usage: python assembler.py <input.as> <output.mc>")
    assemble(sys.argv[1], sys.argv[2])

