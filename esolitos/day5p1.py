# noinspection SpellCheckingInspection
test_data = {
    "FBFBBFFRLR": {
        'row': 44,
        'col': 5,
        'id': 357
    },
    "BFFFBBFRRR": {
        'row': 70,
        'col': 7,
        'id': 567
    },
    "FFFBBBFRRR": {
        'row': 14,
        'col': 7,
        'id': 119
    },
    "BBFFBBFRLL": {
        'row': 102,
        'col': 4,
        'id': 820
    },
}


def parse(code: str) -> int:
    _, _, seat_id = parse_all(code)
    return seat_id


def parse_all(code: str) -> tuple:
    row_code = code[:7]
    col_code = code[7:]

    row = parse_row(row_code)
    col = parse_col(col_code)
    seat_id = get_uid(row, col)

    print(f"{code}: row {row}, column {col}, seat ID {seat_id}")
    return row, col, seat_id


def parse_row(seat_code: str):
    return parse_bsp(seat_code, use_lower='F', use_upper='B')


def parse_col(seat_code: str):
    return parse_bsp(seat_code, use_lower='L', use_upper='R')


def parse_bsp(bsp_code: str, use_lower: str, use_upper: str, num_range: (int, int) = None) -> int:
    from math import ceil
    [n_min, n_max] = num_range if (num_range is not None) else (0, (pow(2, len(bsp_code)) - 1))

    char = bsp_code[0]
    if char == use_lower:
        n_max -= int(ceil((n_max - n_min) / 2))
    elif char == use_upper:
        n_min += int(ceil((n_max - n_min) / 2))
    else:
        raise RuntimeError(f"Unexpected char: " + char)

    if n_min == n_max or len(bsp_code) <= 1:
        return n_max

    return parse_bsp(bsp_code[1:], use_lower, use_upper, (n_min, n_max))


def get_uid(seat: int, col: int) -> int:
    return (seat * 8) + col


if __name__ == '__main__':
    data = open('./input/5.txt')
    for code in test_data:
        [row, col, seat] = parse_all(code.strip())
        check_data = test_data[code]
        if row != check_data.get('row'):
            print(check_data)
            raise RuntimeError('Invalid ROW: ' + row)
        if col != check_data.get('col'):
            print(check_data)
            raise RuntimeError('Invalid COL: ' + col)
        if seat != check_data.get('id'):
            print(check_data)
            raise RuntimeError('Invalid ID: ' + seat)

    print("### ### END TEST DATA ### ###")

    max_id = 0
    for code in data:
        max_id = max(max_id, parse(code.strip()))

    print(max_id)
