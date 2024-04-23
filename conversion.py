import math

## n decimal and 1 < b < 37 and n belongs to Z ##
def decimal_to_b(n: int, b: int):
    symbol = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    quotient = n // b
    remainder = n % b
    result = str(symbol[remainder])
    while quotient != 0:
        remainder = quotient % b
        quotient = quotient // b
        result += str(symbol[remainder])
    return result[::-1]

## 1 < b < 37 and n belongs to Z ##
def evaluate(b: int, n: str):
    symbol = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    n = list(n)
    length = len(n)
    result = 0
    for i in range(length):
        result += symbol.index(n[length - 1 - i]) * (b ** i)
    return result

## have to pass through decimal conversion first ##
def b_to_b1(n, b, b1):
    return decimal_to_b(evaluate(b, n), b1)

# print(b_to_b1(input(), int(input()), int(input())))
########################################################################

## xth-root of n = c ? ##
def nth_root(n: int, c: int):
    x = 2
    while n ** (1 / x) != c:
        x += 1
    return x

## p: 2 power (2^c=p, c belongs to N*\{1}), 1 < p < 37 ##
def binary_to_p(n: str, p):
    symbol = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    root = nth_root(p, 2)
    while len(n) % root != 0:
        n = '0' + n
    n = list(n)
    result = ''
    for i in range(len(n)):
        if (i + 1) % root == 0:
            result += symbol[evaluate(2, ''.join(n[i + 1 - root : i + 1]))]
    return result

# print(binary_to_p(input(), int(input())))
########################################################################

## decimal number, ex: 0.625, n > 0 ##
def decimal_to_binary(n: float):
    binary = str(decimal_to_b(math.floor(n), 2))
    n = n - math.floor(n)
    n = n * 2
    integer_part = math.floor(n)
    fractional_part = n - integer_part
    result = binary + '.' + str(integer_part)
    while fractional_part != 0:
        n = fractional_part * 2
        integer_part = math.floor(n)
        fractional_part = n - integer_part
        result += str(integer_part)
    return result

# print(decimal_to_binary(float(input())))