import re

def check_input_format(line):
    split_list = line.split()
    if len(split_list) != 3:
        return False

    value = split_list[-1]

    if re.match("^\d+?\.\d+?$", value) is None:
        return value.isdigit()

    return True

def new_block_log(block, state):
    print("new block enter blockchain:")
    block.dump()
    state.dump()
    print()

def read_from_file(input_str):
    try:
        with open(input_str) as f:
            txs = []
            for line in f:
                if check_input_format(line):
                    from_adress, to_address, amount_str = line.split()
                    amount = float(amount_str)

                    txs.append((from_adress, to_address, amount))
                else:
                    print("input format error")
            f.close()
            return txs
    except FileNotFoundError:
        print("input file not found")
        return []
