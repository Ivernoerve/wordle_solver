import re
from string import ascii_lowercase
import numpy as np
import pandas as pd





def sep(word):
    return [char for char in word]


def get_5_letter_words(txt_file: str) -> list:
    with open("words.txt", "r") as file:
        words = []
        for row in file:
            
            
            #if len(text) == 5 and text.islower():
            words.append(row.strip())

        reg_filter = "^[a-z]{5,5}$"

        condition = re.compile(reg_filter)

        five_letter_words = list(filter(condition.match, words)) 
    
    return five_letter_words


def get_letter_index_frequency(word_list: list) -> list:
    letter_count_df = pd.DataFrame(0,index = np.arange(5), columns=list(ascii_lowercase))
    

    for word in word_list:
        for i, l in enumerate(word):
            letter_count_df[l][i] += 1
            

    return letter_count_df


def sort_by_letter_index_probability(letter_count_df, word_list):

    letter_probability_df = letter_count_df / len(word_list)

    word_values = []

    for word in word_list:

        score = 0
        for i, l in enumerate(word):
            
            score += letter_probability_df[l][i] * letter_probability_df[l].sum()

        word_values.append(score)

    sorted_words = [word for _, word in sorted(zip(word_values, word_list))]
    sorted_words.reverse()

    return sorted_words
    
    




def sort_by_letter_frequency(word_list: list) -> list:
    letter_frequency_dict = {letter: 0 for letter in ascii_lowercase}

    
    for word in word_list:
        letters = sep(word)
        unique = np.unique(letters)
        
        for letter in unique:
           letter_frequency_dict[letter] += 1


    letter_sum = np.sum(list(letter_frequency_dict.values()))

    letter_value_dict = {letter: value / letter_sum for letter, value in zip(ascii_lowercase, list(letter_frequency_dict.values()))}



    word_values = []
    for word in word_list:
        letters = sep(word)
        
        value = 0
        for letter in np.unique(letters):
            value += letter_value_dict[letter]
        
        word_values.append(value)

    sorted_words = [word for _, word in sorted(zip(word_values, word_list))]

    sorted_words.reverse()
    return sorted_words

        
def sort_by_entropy(letter_count_df, word_list):
    letter_probability_df = letter_count_df / len(word_list)

    word_values = []

    for word in word_list:

        score = 0
        for i, l in enumerate(word):
            score -= letter_probability_df[l][i] * np.log2(letter_probability_df[l][i])

        word_values.append(score)
    sorted_words = [word for _, word in sorted(zip(word_values, word_list))]
    sorted_words.reverse()

    return sorted_words


if __name__ == "__main__":
    pass


