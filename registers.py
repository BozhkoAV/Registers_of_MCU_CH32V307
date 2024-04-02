import glob
import json
import argparse
import os


def load_register_data(group):
    try:
        with open(f"register_groups/{group}.json", 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise Exception(f"Error: Register group '{group}' not found.")


def display_group_info(group):
    register_data = load_register_data(group)

    print("\nName of registers group:")
    print(register_data['name'])

    print("\nRegisters:")
    for register in register_data['registers']:
        print(f"{register} - {register_data['registers'][register]['name']}")
    print()


def display_register_info(group, register):
    register_data = load_register_data(group)

    if register not in register_data['registers']:
        raise Exception(f"Error: Register '{register}' not found in group '{group}'.\n")

    print(f"\n{group.upper()} -> {register.upper()}")

    print("\nName of register:")
    print(register_data['registers'][register]['name'])

    print("\nBits:")
    for bit_name, bit_info in register_data['registers'][register]['bits'].items():
        print(f"{bit_info['position']} - {bit_name} - {bit_info['name']}")
    print()


def display_bit_info(group, register, bit):
    register_data = load_register_data(group)

    if register not in register_data['registers']:
        raise Exception(f"Error: Register '{register}' not found in group '{group}'.\n")

    if bit not in register_data['registers'][register]['bits']:
        raise Exception(f"Error: Bit '{bit}' not found in register '{register}' of group '{group}'.\n")

    print(f"\n{group.upper()} -> {register.upper()} -> {bit.upper()}")

    print(f"\nName of register: {register_data['registers'][register]['name']}")

    bit_info = register_data['registers'][register]['bits'][bit]

    if ":" in str(bit_info['position']):
        print(f"\nInfo about group of bits: {bit_info['name']}.")
    else:
        print(f"\nInfo about bit: {bit_info['name']}.")

    print(f"\nPosition: {bit_info['position']}")
    print(f"\nAccess: {bit_info['access']}")

    if str(bit_info['values']) != "{}":
        print("\nValues:")
        for value, description in bit_info['values'].items():
            print(f"{value}: {description}")

    if str(bit_info['comment']) != "":
        print("\nComment:")
        print(bit_info['comment'])
    print()


def display_bit_value_info(group, register, bit, bin_value):
    register_data = load_register_data(group)

    if register not in register_data['registers']:
        raise Exception(f"Error: Register '{register}' not found in group '{group}'.\n")

    if bit not in register_data['registers'][register]['bits']:
        raise Exception(f"Error: Bit '{bit}' not found in register '{register}' of group '{group}'.\n")

    print(f"\n{group.upper()} -> {register.upper()} -> {bit.upper()}")

    print(f"\nName of register: {register_data['registers'][register]['name']}")

    bit_info = register_data['registers'][register]['bits'][bit]

    if ":" in str(bit_info['position']):
        print(f"\nInfo about group of bits: {bit_info['name']}.")
    else:
        print(f"\nInfo about bit: {bit_info['name']}.")

    print(f"\nPosition: {bit_info['position']}")
    print(f"\nAccess: {bit_info['access']}")

    if ":" in bit_info['position']:
        pos = str(bit_info['position']).split(":")
        bit_len = int(pos[0]) - int(pos[1]) + 1
    else:
        bit_len = 1

    bin_value_check(bin_value, bit_info, bit_len)

    if str(bit_info['comment']) != "":
        print("\nComment:")
        print(bit_info['comment'])
    print()


def bin_value_check(bin_value, bit_info, bit_len):
    if bin_value == 0:
        dec_value = 0
    else:
        dec_value = int(bin_value, 2)

    flag = True
    if 0 <= dec_value < 2 ** bit_len:
        if str(bit_info['values']) == "{}":
            print(f"\nThe value {bin_value} (HEX: {hex(int(bin_value, 2))[2:]}) is acceptable.")
        else:
            for value, description in bit_info['values'].items():
                if int(value) == 0:
                    if dec_value == 0:
                        print(f"\nValue:\n{value}: {description}")
                        flag = False
                        break
                else:
                    if int(value, 2) == dec_value:
                        print(f"\nValue:\n{value}: {description}")
                        flag = False
                        break

            if flag:
                print(f"\nThe value {bin_value} (HEX: {hex(int(bin_value, 2))[2:]}) is "
                      f"unacceptable because it is not in the list of acceptable values.")
                print("\nAcceptable values:")
                for value, description in bit_info['values'].items():
                    print(f"{value}: {description}")
    else:
        print(f"\nThe value {bin_value} (HEX: {hex(int(bin_value, 2))[2:]}) is "
              f"unacceptable because it is not in the range [{'0' * bit_len} (HEX: 0), "
              f"{bin(2 ** bit_len - 1)[2:]} (HEX: {hex(int(bin(2 ** bit_len - 1)[2:], 2))[2:]})].")
        if str(bit_info['values']) != "{}":
            print("\nAcceptable values:")
            for value, description in bit_info['values'].items():
                print(f"{value}: {description}")


def display_reg_value_info(group, register, bin_value):
    register_data = load_register_data(group)

    if register not in register_data['registers']:
        raise Exception(f"Error: Register '{register}' not found in group '{group}'.\n")

    print(f"\n{group.upper()} -> {register.upper()}")

    print("\nName of register:")
    print(register_data['registers'][register]['name'])

    bin_value = bin_value.zfill(32)
    print(f"\nValue of Register:\n{bin_value} (HEX: {hex(int(bin_value, 2))[2:].zfill(8)})")

    print("\nBits:")
    for bit_name, bit_info in register_data['registers'][register]['bits'].items():
        print(f"~~~\n{bit_info['position']} - {bit_name} - {bit_info['name']}")

        print(f"\nAccess: {bit_info['access']}")

        if ":" in bit_info['position']:
            pos = str(bit_info['position']).split(":")
            bit_len = int(pos[0]) - int(pos[1]) + 1
            bin_value_check(bin_value[31 - int(pos[0]):31 - int(pos[1]) + 1], bit_info, bit_len)
        else:
            bit_len = 1
            bin_value_check(bin_value[31 - int(bit_info['position'])], bit_info, bit_len)

        if str(bit_info['comment']) != "":
            print("\nComment:")
            print(bit_info['comment'])
        print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-info", "-i", action='store_true',
                        help="display information about available groups of registers")
    parser.add_argument("-tree", "-t", action='store_true',
                        help="display all information about groups of registers as tree")
    parser.add_argument("-group", "-g", metavar="GROUP_NAME",
                        nargs=1, help="display information about group of registers")
    parser.add_argument("-register", "-r", metavar=('GROUP_NAME', 'REGISTER_NAME'),
                        nargs=2, help="display information about register")
    parser.add_argument("-bit", "-b", metavar=('GROUP_NAME', 'REGISTER_NAME', 'BIT_NAME'),
                        nargs=3, help="display information about bit or group of bits")
    parser.add_argument("-hex", metavar=('GROUP_NAME', 'REGISTER_NAME', 'BIT_NAME', "HEX_VALUE"),
                        nargs=4, help="display information about hexadecimal value of bit")
    parser.add_argument("-bin", metavar=('GROUP_NAME', 'REGISTER_NAME', 'BIT_NAME', "BIN_VALUE"),
                        nargs=4, help="display information about binary value of bit")
    parser.add_argument("-regh", "-rh", metavar=('GROUP_NAME', 'REGISTER_NAME', "HEX_VALUE"),
                        nargs=3, help="display information about hexadecimal value of register")
    parser.add_argument("-regb", "-rb", metavar=('GROUP_NAME', 'REGISTER_NAME', "BIN_VALUE"),
                        nargs=3, help="display information about binary value of register")
    args = parser.parse_args()

    try:
        if args.info:
            fun_info()
        if args.tree:
            fun_tree()
        if args.group:
            fun_group(args.group)
        if args.register:
            fun_register(args.register)
        if args.bit:
            fun_bit(args.bit)
        if args.hex:
            fun_hex(args.hex)
        if args.bin:
            fun_bin(args.bin)
        if args.regh:
            fun_regh(args.regh)
        if args.regb:
            fun_regb(args.regb)
    except Exception as e:
        print(e)


def fun_info():
    json_files = glob.glob(os.path.join("register_groups", '*.json'))

    if len(json_files) != 0:
        print("\nRegister groups:")
        for file_name in [os.path.splitext(os.path.basename(file))[0] for file in json_files]:
            print(file_name)
        print()
    else:
        print("JSON files weren't found in the register_groups directory.")


def fun_tree():
    json_files = glob.glob(os.path.join("register_groups", '*.json'))

    if len(json_files) != 0:
        for group in [os.path.splitext(os.path.basename(file))[0] for file in json_files]:
            print(f"─── {group}")
            register_data = load_register_data(group)
            for register in register_data['registers']:
                print(f"   └── {register}")
                for bit in register_data['registers'][register]['bits']:
                    print(f"      └── {bit} {register_data['registers'][register]['bits'][bit]['position']}")
        print()
    else:
        print("JSON files weren't found in the register_groups directory.")


def fun_group(args):
    group_name = str(args[0]).upper()
    display_group_info(group_name)


def fun_register(args):
    group_name = str(args[0]).upper()
    reg_name = str(args[1]).upper()
    display_register_info(group_name, reg_name)


def fun_bit(args):
    group_name = str(args[0]).upper()
    reg_name = str(args[1]).upper()
    bit_name = str(args[2]).upper()
    display_bit_info(group_name, reg_name, bit_name)


def fun_hex(args):
    group_name = str(args[0]).upper()
    reg_name = str(args[1]).upper()
    bit_name = str(args[2]).upper()
    hex_value = str(args[3]).upper()
    if all(c.isdigit() or c.isalpha() and c in 'ABCDEF' for c in hex_value):
        hex_value = hex_value.lstrip('0')
        if len(hex_value) == 0:
            bin_value = 0
        else:
            bin_value = bin(int(hex_value, 16))[2:]
        display_bit_value_info(group_name, reg_name, bit_name, bin_value)
    else:
        raise Exception("Error: Value is not a hexadecimal number.")


def fun_bin(args):
    group_name = str(args[0]).upper()
    reg_name = str(args[1]).upper()
    bit_name = str(args[2]).upper()
    bin_value = str(args[3])
    if all(c.isdigit() and c in '01' for c in bin_value):
        bin_value = bin_value.lstrip('0')
        if len(bin_value) == 0:
            bin_value = 0
        display_bit_value_info(group_name, reg_name, bit_name, bin_value)
    else:
        raise Exception("Error: Value is not a binary number.")


def fun_regh(args):
    group_name = str(args[0]).upper()
    reg_name = str(args[1]).upper()
    hex_value = str(args[2]).upper()
    if all(c.isdigit() or c.isalpha() and c in 'ABCDEF' for c in hex_value):
        hex_value = hex_value.lstrip('0')
        if len(hex_value) == 0:
            bin_value = 0
        else:
            bin_value = bin(int(hex_value, 16))[2:]
        display_reg_value_info(group_name, reg_name, bin_value)
    else:
        raise Exception("Error: Value is not a hexadecimal number.")


def fun_regb(args):
    group_name = str(args[0]).upper()
    reg_name = str(args[1]).upper()
    bin_value = str(args[2])
    if all(c.isdigit() and c in '01' for c in bin_value):
        bin_value = bin_value.lstrip('0')
        if len(bin_value) == 0:
            bin_value = 0
        display_reg_value_info(group_name, reg_name, bin_value)
    else:
        raise Exception("Error: Value is not a binary number.")


if __name__ == "__main__":
    main()
