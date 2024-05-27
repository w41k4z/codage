def get_suffixes(L1: list[str], L2: list[str], ignore_epsilon: bool = True):
    Lx = {}
    for u in L1:
        for each in L2:
            if each.startswith(u):
                x = each[len(u):]
                if not ignore_epsilon and x == '':
                    raise Exception(u)
                if x != '' and x not in Lx.values():
                    Lx[each + '-' + u] = x
    return Lx

def is_code(L: list[str]):
    if L == ['']:
        return False
    Ls = {}
    index = 1
    L1 = get_suffixes(L, L)
    if len(L1.values()) == 0:
        return True
    Ls[str(index)] = L1
    index += 1
    suffixes = {'-'.join(L1.values()): True}
    while True:
        previous_L = Ls[str(index - 1)]
        previous_L_values = list(previous_L.values())
        try:
            _ = get_suffixes(L, previous_L_values, False)
            __ = get_suffixes(previous_L_values, L, False)
            current = list(_.values()) + list(__.values())
            if current:
                try:
                    suffixes['-'.join(current)]
                    return True
                except:
                    merged = _.copy()
                    merged.update(__)
                    suffixes['-'.join(current)] = True
                    Ls[str(index)] = merged
                    index += 1
            else:
                return True
        except Exception as e:
            df = ''
            i = index - 1
            u = e.args[0]
            while i > 0:
                prev_L = Ls[str(i)]
                for key, value in prev_L.items():
                    if value == u:
                        anomaly, u = key.split('-')
                        if i == 1:
                            anomaly += u
                        df = anomaly + df
                        break
                i -= 1
            print('Source: ' + df)
            return False

def possibilities(i: int, L):
    if i == 0:
        raise Exception('i must be greater than 0')
    p = []
    if i == 1:
        for index in range(len(L)):
            c = L.copy()
            c.pop(index)
            p.append(c)
    else:
        for index in range(len(L)):
            c = L.copy()
            c.pop(index)
            for each in possibilities(i - 1, c):
                p.append(each)
    return p
    
def pop_until_code(L):
    i = 1
    while i < len(L):
        p = possibilities(i, L)
        for possibility in p:
            if is_code(possibility):
                diff = []
                for each in L:
                    if each not in possibility:
                        diff.append(each)
                return i, diff, possibility 
        i += 1
    return -1
    

# L = ['0', '01', '100', '010']
# # L = ['1', '00', '01', '10']
# # L = ['0', '100', '010']
# print(is_code(L))
# print(pop_until_code(L))