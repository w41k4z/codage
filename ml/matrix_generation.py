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
    
    # Character frequency distribution
    char_freq = {'0': 0, '1': 0}
    for word in language:
        for char in word:
            char_freq[char] += 1
    
    max_char_freq = max(char_freq.values())
    min_char_freq = min(char_freq.values())
    char_freq_std = np.std(list(char_freq.values()))
    
    return [
        length_mean, length_std, max_length, min_length,
        max_char_freq, min_char_freq, char_freq_std
    ]
    
def generate_random_training_data():
    with open('data/random_training.csv', 'w') as w:
        w.write('length_mean;length_std;max_length;min_length;max_char_freq;min_char_freq;char_freq_std;code\n')
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
        w.write('length_mean;length_std;max_length;min_length;max_char_freq;min_char_freq;char_freq_std;code\n')
        with open('raw_data/raw_training_code.data', 'r') as r:
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

def generate_test_data():
    with open('data/test.csv', 'w') as w:
        w.write('length_mean;length_std;max_length;min_length;max_char_freq;min_char_freq;char_freq_std;code\n')
        with open('datanotprepared/codeDatas.txt', 'r') as code_file, open('datanotprepared/notCodeDatas.txt', 'r') as non_code_file:
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
                
generate_random_training_data()
generate_training_data()
generate_test_data()