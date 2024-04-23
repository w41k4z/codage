from conversion import decimal_to_b, decimal_to_binary

def binary_addition(a, b):
    if a == '1' and b == '1':
        return '10'
    elif a == '0' and b == '0':
        return '00'
    else:
        return '01'      

def addition(a: str, b: str):
    a = list(a)
    b = list(b)
    result = []
    remaining = '0'
    i = len(a) - 1
    j = len(b) - 1
    while i >= 0 and j >= 0:
        addition1 = binary_addition(a[i], b[j])
        addition2 = binary_addition(addition1[1], remaining)
        remaining = binary_addition(addition1[0], addition2[0])[1]
        result.append(addition2[1])
        i -= 1
        j -= 1
    while i >= 0:
        addition1 = binary_addition(a[i], remaining)
        remaining = addition1[0]
        result.append(addition1[1])
        i -= 1
    while j >= 0:
        addition1 = binary_addition(b[j], remaining)
        remaining = addition1[0]
        result.append(addition1[1])
        j -= 1
    if remaining == '1':
        result.append(remaining)
    return ''.join(result[::-1])

def binary_representation_8bits_16bits(n: str):
    is_negative = False
    if n[0] == '-':
        is_negative = True
    if is_negative:
        n = n.replace('-', '')
    binary = decimal_to_b(int(n), 2)
    length = len(binary)
    limit = 8 - length if length < 8 else 16 - length
    for i in range(limit):
        binary = '0' + binary
    if is_negative:
        binary = list(binary)
        for i in range(len(binary)):
            if binary[i] == '0':
                binary[i] = '1'
            else:
                binary[i] = '0'
        binary = ''.join(binary)
        binary = addition(binary, '1')
    return binary

# print(binary_representation_8bits_16bits(input()))

## n belongs Z ##
def IEEE_754_representation_32bits(n: str):
    bias = 127
    sign = 1 if n[0] == '-' else 0
    n = decimal_to_binary(float(n.replace('-', '')))
    integer_part, fractional_part = n.split('.')
    e = 0
    if integer_part == '0':
        for i in range(len(fractional_part)):
            if fractional_part[i] == '1':
                e = -1 * (i + 1)
                break
    elif len(integer_part) > 1:
        e = len(integer_part) - 1
    n = n.replace('.', '')
    start_index = len(integer_part) - e
    if start_index == len(n):
        n += '0'
    mantiss = n[start_index:]
    mantiss = mantiss + ('0' * (23 - len(mantiss)))
    exponent = decimal_to_b(bias + e, 2)
    representation = str(sign) + str(exponent) + mantiss
    arr = []
    for i in range(len(representation)):
        if (i + 1) % 8 == 0:
            arr.append(representation[i - 7 : i + 1])
        i += 1
    return ' '.join(arr)[:33 + 3] # for irrational number safety

print(IEEE_754_representation_32bits(input()))