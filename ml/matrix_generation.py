from sardinas import is_code
import numpy as np
import ast

def get_numeric_definition(language: list[str]):
    lengths = [len(word) for word in language]
    length_mean = np.mean(lengths)
    length_std = np.std(lengths)
    max_length = max(lengths)
    min_length = min(lengths)
    
    # Overlap properties
    # prefix_count = sum(1 for i in range(len(language)) for j in range(len(language)) if i != j and language[i].startswith(language[j]))
    # suffix_count = sum(1 for i in range(len(language)) for j in range(len(language)) if i != j and language[i].endswith(language[j]))
    
    # character frequency standard deviation
    zero_chars = []
    one_chars = []
    for word in language:
        zero = word.count('0')
        one = word.count('1')
        zero_chars.append(zero / len(word))
        one_chars.append(one / len(word))
    zero_char_freq_std = np.std(zero_chars)
    one_char_freq_std = np.std(one_chars)
    
    # Global character frequency distribution
    global_char_freq = {'0': 0, '1': 0}
    for word in language:
        for char in word:
            global_char_freq[char] += 1
    global_zero_character_freq = global_char_freq['0']
    global_one_character_freq = global_char_freq['1']
    char_freq_std = np.std(list(global_char_freq.values()))
    
    return [
        length_mean, length_std, max_length, min_length,
        global_zero_character_freq, global_one_character_freq, char_freq_std,
        zero_char_freq_std, one_char_freq_std,
        # prefix_count, suffix_count
    ]
    
def generate_random_training_data():
    with open('data/random_training.csv', 'w') as w:
        w.write('length_mean;length_std;max_length;min_length;global_zero_character_freq;global_one_character_freq;char_freq_std;zero_char_freq_std;one_char_freq_std;code\n')
        with open('raw_data/total_random_codes.data', 'r') as r:
            for i in range(2500):
                language = r.readline().split()
                code = 1 if is_code(language) else 0
                numeric_definition = get_numeric_definition(language)
                numeric_definition.append(code)
                w.write(';'.join([str(x) for x in numeric_definition]) + '\n')
        r.close()
        with open('raw_data/total_random_non_codes.data', 'r') as r:
            for i in range(2500):
                language = r.readline().split()
                code = 1 if is_code(language) else 0
                numeric_definition = get_numeric_definition(language)
                numeric_definition.append(code)
                w.write(';'.join([str(x) for x in numeric_definition]) + '\n')
        r.close()
    w.close()
    
def generate_training_data():
    with open('data/training.csv', 'w') as w:
        w.write('length_mean;length_std;max_length;min_length;global_zero_character_freq;global_one_character_freq;char_freq_std;zero_char_freq_std;one_char_freq_std;code\n')
        with open('raw_data/raw_training_code.data', 'r') as r:
            for _ in range(2500):
                language = r.readline().split()
                code = 1 if is_code(language) else 0
                numeric_definition = get_numeric_definition(language)
                numeric_definition.append(code)
                w.write(';'.join([str(x) for x in numeric_definition]) + '\n')
        r.close()
        with open('raw_data/total_random_non_codes.data', 'r') as r:
            for i in range(2500):
                language = r.readline().split()
                code = 1 if is_code(language) else 0
                numeric_definition = get_numeric_definition(language)
                numeric_definition.append(code)
                w.write(';'.join([str(x) for x in numeric_definition]) + '\n')
        r.close()
    w.close()

def generate_test_data():
    with open('data/test.csv', 'w') as w:
        w.write('length_mean;length_std;max_length;min_length;global_zero_character_freq;global_one_character_freq;char_freq_std;zero_char_freq_std;one_char_freq_std;code\n')
        with open('test/codeDatas.txt', 'r') as code_file, open('test/notCodeDatas.txt', 'r') as non_code_file:
            for line in code_file:
                language = ast.literal_eval(line.strip())
                code = 1 if is_code(language) else 0
                numeric_definition = get_numeric_definition(language)
                numeric_definition.append(code)
                w.write(';'.join([str(x) for x in numeric_definition]) + '\n')
            for line in non_code_file:
                language = ast.literal_eval(line.strip())
                code = 1 if is_code(language) else 0
                numeric_definition = get_numeric_definition(language)
                numeric_definition.append(code)
                w.write(';'.join([str(x) for x in numeric_definition]) + '\n')
                
# generate_random_training_data()
generate_training_data()
generate_test_data()