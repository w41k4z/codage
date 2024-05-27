from joblib import load
import numpy as np
from sardinas_paterson import is_code

class AI:
    
    def __init__(self):
      self.model = load('../model.joblib')
    
    def get_numeric_definition(language: list[str]):
        lengths = [len(word) for word in language]
        length_mean = np.mean(lengths)
        length_std = np.std(lengths)
        max_length = max(lengths)
        min_length = min(lengths)
        
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
    
    def predict(self, language: list[str]):
        numeric_definition = AI.get_numeric_definition(language)
        prediction = True if self.model.predict(np.array([numeric_definition]))[0] == 1 else False
        return is_code(language), prediction