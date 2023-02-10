from selenium.webdriver.common.by import By
from itertools import compress 

import re
import time


import numpy as np

from html_parser_class import Browser
from word_values import sort_by_letter_index_probability,sort_by_letter_frequency , get_letter_index_frequency, sort_by_entropy


def remove_popups(webdriver: Browser):
    """
    Function to remove the popups prior to solving the wordle.

    webdriver: Browser represented by the browser class
    """

    webdriver.select_item('pz-gdpr-btn-closex', By.ID).click()
    webdriver.select_item('game-icon', By.CLASS_NAME).click()
    time.sleep(1)

    return 1


def guess_word(webdriver: Browser, word: str):
    """
    Function to input a guess and return the response.

    webdriver: Browser represented by the browser class
    word: word to guess
    """

    webdriver.input_text('body', By.TAG_NAME, word)
    time.sleep(2)

    return 1

def delete_word(webdriver: Browser):
    '''
    Function to delete illegal guesses
    webdriver: Browser represented by the browser class
    '''
    webdriver.delete_text('body', By.TAG_NAME, 5)

    return 1
    

def get_response(webdriver: Browser, row_number: int) -> list:
    

    time.sleep(2)
    table = webdriver.select_item('Board-module_board__jeoPS', By.CLASS_NAME)
    row = table.find_element(By.CSS_SELECTOR,  f"[aria-label='Row {row_number}']")

    text = lambda element: webdriver.browser.execute_script("return arguments[0].innerHTML;", element)


    responses = re.findall('data-state="(.*?)"', text(row))
    print(responses)

    return responses


def get_regex_filter(current_filter: list, responses: list, guessed_word: list, correct_tracker: list) -> list:
    '''
    Function to create the regex filter to filter out wrong words
    current_filter: The filter from the prior iteration
    guessed_word: The word guessed to pricuce the responses 
    responses: responses from wordle by the current guess
    
    ---
    returns list with filter components in each index
    '''

    for i, response in enumerate(responses):

        if response == 'correct' and not correct_tracker[i]:
            print('correct')
            if f'(?=.*{guessed_word[i]}' in current_filter:
                current_filter.remove(f'(?=.*{guessed_word[i]})')
            
            if f'(?!.*{guessed_word[i]}' in current_filter:
                current_filter.remove(f'(?!.*{guessed_word[i]})')
            
            correct_tracker[i] = 1
            current_filter[i-5] = guessed_word[i]


        elif response == 'present':
            
            print('present', i, guessed_word[i], guessed_word)
            if f'(?=.*{guessed_word[i]}' not in current_filter:
                current_filter.insert(0, f'(?=.*{guessed_word[i]})')

            if current_filter[i-5] == '.':
                current_filter[i-5] = f'[^{guessed_word[i]}]'
            else:
                to_mod = list(current_filter[i-5])
                to_mod.insert(-1, guessed_word[i])
                current_filter[i-5] = ''.join(to_mod)

            
        elif response == 'absent' and guessed_word[i] not in list(compress(guessed_word, correct_tracker)):
            current_filter.insert(-5, f'(?!.*{guessed_word[i]})')


    return current_filter, correct_tracker


def filter_words(word_list: list, regex_filter: str) -> list:
    '''
    function to remove words not fitting to the regex filter
    word_list: list of words to be filtered
    regex_filter: filter to remove impossible matches
    ---
    returns a new list of words sorted by index probability
    '''
    pattern = re.compile(''.join(regex_filter))
    print(pattern)
    filtered_word_list = list(filter(pattern.match, word_list)) 
    print("old / new word count")
    print(len(word_list) ,len(filtered_word_list))

    sorted_filtered_word_list = sort_by_letter_frequency(filtered_word_list)
    #new_letter_index_frequency = get_letter_index_frequency(filtered_word_list)
    #sorted_filtered_word_list = sort_by_entropy(
    #                                        new_letter_index_frequency, 
    #                                        filtered_word_list)
    
    return sorted_filtered_word_list


def run():

    reg_filter = ['.', '.', '.', '.', '.']
    correct_tracker = np.zeros(5, dtype = int)
    incorrect_words = []


    sorted_words = np.loadtxt('sorted_words.csv', dtype=str)
    wordle_driver = Browser('https://www.nytimes.com/games/wordle/index.html')

    remove_popups(wordle_driver)
    time.sleep(1)
    word_to_guess = 'arose'

    for turn in range(1,6):
        print(f'\nturn {turn}\n')
        
        guess_word(wordle_driver, word_to_guess)


        responses = get_response(wordle_driver, turn)

        while 'tbd' in responses or 'empty' in responses:
            incorrect_words.append(word_to_guess)
            del(sorted_words[0])
            word_to_guess = sorted_words[0]
            delete_word(wordle_driver)
            guess_word(wordle_driver, word_to_guess)

            responses = get_response(wordle_driver, turn)



        reg_filter, correct_tracker = get_regex_filter(reg_filter, responses, word_to_guess, correct_tracker)
    

        sorted_words = filter_words(sorted_words, reg_filter)
        print(sorted_words[0])
        

        word_to_guess = sorted_words[0]
        time.sleep(1)

        if sum(correct_tracker) == 5:
            print('game won')
            break 

    if len(incorrect_words) > 0:
        word_list = list(np.loadtxt('sorted_words.csv', dtype=str))
        for word in incorrect_words:
            word_list.remove(word)


        np.savetxt('sorted_words.csv', word_list, delimiter=',', fmt ='% s')


    
    return 1

if __name__ == '__main__':
    run()

