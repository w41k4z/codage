import random
from sardinas import is_code

def generate_binary_word(min_length = 1, max_length = 7):
    length = random.randint(min_length, max_length)
    word = ''.join(random.choices('01', k=length))
    return word

def generate_specific_binary_word(word_length: int):
    if word_length < 1:
        raise ValueError('Word length has to be greater than 0')
    return ''.join(random.choices('01', k=word_length))
    

def generate_language(min_word_count = 1, max_word_count = 10):
    num_words = random.randint(min_word_count, max_word_count)
    language = set()
    while len(language) < num_words:
        word = generate_binary_word()
        language.add(word)
    return list(sorted(language, key = lambda x: len(x)))

def generate_specific_language(word_count: int, word_length: int):
    if word_count < 1:
        raise ValueError('Word count has to be greater than 0')
    language = set()
    while len(language) < word_count:
        word = generate_specific_binary_word(word_length)
        language.add(word)
    return list(sorted(language, key = lambda x: len(x)))
    
def generate_prefixed_language(min_word_count = 1, max_word_count = 10):
    num_words = random.randint(min_word_count, max_word_count)
    language: set[str] = set()
    while len(language) < num_words:
        word = generate_binary_word()
        is_prefix = False
        for each in language:
            if each.startswith(word):
                is_prefix = True
                break
        if not is_prefix:
            language.add(word)
    return list(sorted(language, key = lambda x: len(x)))

def generate_code_language():
    while True:
        language = generate_language()
        if is_code(language):
            return language

def generate_non_code_language():
    while True:
        language = generate_language()
        if is_code(language):
            continue
        return language
        
def generate_languages(x: int):
    unique_languages = set()
    while len(unique_languages) < x:
        language = tuple(generate_language())
        unique_languages.add(language)
    return [list(language) for language in unique_languages]

def generate_specific_languages(x: int, word_count: int, word_length: int):
    if 2 ** word_length - 1 < word_count * x:
        x = 2 ** word_length - 1
    unique_languages = set()
    while len(unique_languages) < x:
        language = tuple(generate_specific_language(word_count, word_length))
        unique_languages.add(language)
    return [list(language) for language in unique_languages]

################################################################################

## RANDOMS ##

def generate_total_random():
    def generate_random_code_languages():
        unique_languages = set()
        while len(unique_languages) < 2500:
            language = generate_code_language()
            unique_languages.add(tuple(language))
        return [list(language) for language in unique_languages]

    def generate_random_non_code_languages():
        unique_languages = set()
        while len(unique_languages) < 2500:
            language = generate_non_code_language()
            unique_languages.add(tuple(language))
        return [list(language) for language in unique_languages]
    
    with open('raw_data/total_random_codes.data', 'w') as file:
        for language in generate_random_code_languages():
            file.write(' '.join(language) + '\n')
        print('2500 code languages generated')
        file.close()
        
    with open('raw_data/total_random_non_codes.data', 'w') as file:
        for language in generate_random_non_code_languages():
            file.write(' '.join(language) + '\n')
        print('2500 non code languages generated')
        file.close()
        
        
################################################################################

        
## CLEANED VERSION ##

def generate_training_data():
    # 248
    def generate_single_element_languages():
        # including 1 length code directly
        languages = set([tuple(['0']), tuple(['1'])])
        for i in range(2, 8):
            for language in generate_specific_languages(float('inf'), 1, i):
                languages.add(tuple(language))
        return languages
    
    # 500
    def generate_fixed_length_languages():
        # including 2 length code directly
        languages = set([tuple(['00']), tuple(['01']), tuple(['10']), tuple(['11'])])
        while(len(languages) < 500):
            word_count = random.randint(2, 7)
            word_length = random.randint(3, 10)
            languages.add(tuple(generate_specific_language(word_count, word_length)))
        print('tonga')
        return languages
    
    # 1000
    def generate_prefixed_languages(languages_set: set[tuple[str]]):
        initial_length = len(languages_set)
        while len(languages_set) - initial_length < 1000:
            languages_set.add(tuple(generate_prefixed_language()))
    
    # 752
    def generate_random_languages(prefixed_languages: set[tuple[str]]):
        initial_length = len(prefixed_languages)
        while len(prefixed_languages) - initial_length < 752:
            prefixed_languages.add(tuple(generate_code_language()))

    single_element_languages = generate_single_element_languages()
    fixed_length_languages = generate_fixed_length_languages()
    generate_prefixed_languages(fixed_length_languages) # adding all prefixed languages to the fixed length languages
    generate_random_languages(fixed_length_languages) # adding all random code languages to the prefixed languages
    
    with open('raw_data/raw_training_code.data', 'w') as file:
        for language in single_element_languages:
            file.write(' '.join(language) + '\n')
        for language in fixed_length_languages:
            file.write(' '.join(language) + '\n')
        file.close()
    
generate_total_random()
generate_training_data()