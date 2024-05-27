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
    language = ['100110', '11', '010001', '1000', '0111']
    # ['11001', '1000100', '010100', '0', '00001']
    # ['11001', '1000100', '010100', '0', '00001']
    numeric_def = get_numeric_definition(language)
    print(is_code(language))
    print(model.predict(np.array([numeric_def])))

# print(training())
prediction()