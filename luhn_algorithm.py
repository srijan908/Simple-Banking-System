def check_luhn(data):
    n = len(data)-1
    cur = 0
    total = 0

    while n >= 0:
        if cur == 0:
            total += int(data[n])
        else:
            x = int(data[n]) * 2
            if x > 9:
                total += int(x / 10) + (x % 10)
            else:
                total += x
        n -= 1
        cur = not cur

    if total % 10 == 0:
        return True
    return False


def generate(card_no):
    check_sum = 0

    for x in range(1, 16):
        if x % 2 == 1:
            temp = 2 * int(card_no[x - 1])
            if temp > 9:
                temp -= 9
            check_sum += temp
        else:
            check_sum += int(card_no[x - 1])

    if check_sum % 10 == 0:
        card_no += '0'
    else:
        card_no += str(10 - check_sum % 10)

    return card_no
