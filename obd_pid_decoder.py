pid_table = {
    "2105": {
        "name": "engine coolant temp",
        "length": 1,
        "unit": 1,
    },
    "210C": {
        "name": "engine RPM",
        "length": 2,
        "unit": 1,
    },

    "210D": {
        "name": "vehicle speed",
        "length": 1,
        "unit": 1,
    },

    "210F": {
        "name": "intake air temp",
        "length": 1,
        "unit": 1,
    },

    "2110": {
        "name": "air flow rate",
        "length": 2,
        "unit": 0.01,
    },

}


def low_to_high(h):
    h = "".join(reversed([h[i:i + 2] for i in range(0, len(h), 2)]))
    return h


def hex_to_int(h, is_low_to_high=True):
    if len(h) > 2 and h[:2] == "0x":
        if is_low_to_high:
            h = h[:2] + "".join(reversed([h[i:i + 2] for i in range(2, len(h), 2)]))
        return int(h, 0)
    else:
        if is_low_to_high:
            h = "".join(reversed([h[i:i + 2] for i in range(0, len(h), 2)]))
        return int(h, 16)


def decode_pid_type(pid_hex):
    pid_types = []
    for i in range(0, len(pid_hex), 4):
        pid_type = pid_hex[i:i + 4]
        pid_type = low_to_high(pid_type)
        pid_types.append(pid_type)
    return pid_types


def decode_pid_data(pid_hex, pid_types):
    pid_data = {}
    start_idx = 0
    for pid_type in pid_types:
        pid_type = pid_type.upper()
        bytes_size = pid_table[pid_type]["length"]
        end_idx = start_idx + bytes_size * 2
        value = hex_to_int(pid_hex[start_idx:end_idx])
        value = pid_table[pid_type]["unit"] * value
        pid_data[pid_type] = value
        start_idx = end_idx
    return pid_data


if __name__ == "__main__":
    type_data = "05210C210D210F211021"
    print(decode_pid_type(type_data))
    pid_data = "3BE8030064280A"
    print(decode_pid_data(pid_data, decode_pid_type(type_data)))
