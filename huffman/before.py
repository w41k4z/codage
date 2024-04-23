from node import Node

class Huffman:
    
    def __init__(self) -> None:
        self.sp = []
        self.tree = {}
        self.key = ''
    
    def __source(self, information: str):
        source = {}
        for letter in information:
            if letter not in source:
                source[letter] = 1
            else:
                source[letter] += 1
        length = len(information)
        for key in source.keys():
            source[key] /= length
        # sorting each symbols by their probabilities
        self.sp = sorted([(key, value) for key, value in source.items()], key=lambda each: each[1], reverse=True)
    
    def __insert(self, element,  is_asc = True):
        for i in range(len(self.sp)):
            if is_asc:
                if element[1] <= self.sp[i][1]:
                    self.sp.insert(i, element)
                    return
            else:
                if element[1] >= self.sp[i][1]:
                    self.sp.insert(i, element)
                    return
    
    def __huffman_tree(self):
        sp = self.sp.copy()
        for each in self.sp:
            self.tree[each[0]] = Node(each[0], each[1], None, None)
        while len(self.sp) > 1:
            right = self.sp.pop()
            left = self.sp.pop()
            concatenated_symbol = left[0] + '+' + right[0]
            self.tree[concatenated_symbol] = Node(None, right[1] + left[1], None, None)
            self.tree[right[0]].parent, self.tree[right[0]].position  = concatenated_symbol, '0'
            self.tree[left[0]].parent, self.tree[left[0]].position  = concatenated_symbol, '1'
            self.__insert((concatenated_symbol, right[1] + left[1]), False)
        self.sp = sp

    def encode(self, information: str):
        self.__source(information)
        self.__huffman_tree()
        codewords = {}
        for symbol, value in self.sp:
            current_node = self.tree[symbol]
            codeword = ''
            while current_node.parent is not None:
                codeword += current_node.position
                current_node = self.tree[current_node.parent]
            codewords[symbol] = codeword[::-1]
        for key, value in codewords.items():
            self.key += key + '==>>' + value + '|<>|'
        self.key = self.key.removesuffix('|<>|')
        encoded_information = ''
        for letter in information:
            encoded_information += codewords[letter]
        l = 0
        while len(encoded_information) % 8 != 0:
            encoded_information += '0'
            l += 1
        bytes_list = [int(encoded_information[i:i+8], 2) for i in range(0, len(encoded_information), 8)]
        with open('key', 'w') as file:
            file.write(str(l) + '<=>' + self.key)
        bytes_array = bytearray(bytes_list)
        with open('encoded', 'wb') as file:
            file.write(bytes_array)
        return bytes_array
        
    # <symbol1>:<code1>;<symbol2>:<code2> 
    def decode(self, encoded_file_path: str, file_key_path: str):
        l = 0
        with open(file_key_path, 'r') as file:
            l, self.key = file.read().removesuffix('\n').split('<=>')
            l = int(l)
        with open(encoded_file_path, 'rb') as file:
            encoded_information = file.read()
        encoded_information = ''.join(format(byte, '08b') for byte in encoded_information)
        encoded_information = encoded_information[:len(encoded_information) - l]
        huffman_dict = { each.split('==>>')[1]: each.split('==>>')[0] for each in self.key.split('|<>|') }
        decoded_text = ''
        current_bits = ''
        for bit in encoded_information:
            current_bits += bit
            if current_bits in huffman_dict:
                decoded_text += huffman_dict[current_bits]
                current_bits = ""
        return decoded_text
    
huffman = Huffman()
text = ''
with open('test.txt', 'r') as file:
    text = file.read()
# print(text)
huffman.encode(text)
print(huffman.decode('encoded', 'key'))