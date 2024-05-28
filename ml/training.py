import pandas as pd
import numpy as np
from sardinas import is_code

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

def training():
    df_train = pd.read_csv('./data/training.csv', delimiter=';')
    X_train = df_train.iloc[:, :-1].values
    Y_train = df_train.iloc[:, -1].values
    
    df_test = pd.read_csv('./data/test.csv', delimiter=';')
    X_test = df_test.iloc[:, :-1].values
    Y_test = df_test.iloc[:, -1].values
    
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier()
    model.fit(X_train, Y_train)
    
    Y_pred = model.predict(X_test)
    with open('checking', 'w') as c:
        for i in range(len(Y_pred)):
            if (Y_test[i] != Y_pred[i]):
                c.write(str(i + 1) + '\n')
    
    from sklearn.metrics import accuracy_score
    accuracy_score = accuracy_score(Y_test, Y_pred)
    
    import joblib
    joblib.dump(model, 'model.joblib')
    
    return accuracy_score

def prediction():
    from joblib import load
    model = load('model.joblib')
    language = '010101 0101'.split()
    # ['11001', '1000100', '010100', '0', '00001']
    # ['11001', '1000100', '010100', '0', '00001']
    numeric_def = get_numeric_definition(language)
    print(is_code(language))
    print(True if model.predict(np.array([numeric_def]))[0] == 1 else False)

# print(training())
prediction()