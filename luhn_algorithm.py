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
