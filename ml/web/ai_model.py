from joblib import load
import numpy as np
from sardinas_paterson import is_code

class AI:
    
    def __init__(self):
      self.model = load('model.joblib')
    
    def get_numeric_definition(language: list[str]):
        lengths = [len(word) for word in language]
        length_mean = np.mean(lengths)
        length_std = np.std(lengths)
        max_length = max(lengths)
        min_length = min(lengths)
         
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
        ]
    
    def predict(self, language: list[str]):
        numeric_definition = AI.get_numeric_definition(language)
        prediction = True if self.model.predict(np.array([numeric_definition]))[0] == 1 else False
        return is_code(language), prediction