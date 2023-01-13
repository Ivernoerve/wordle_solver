from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time
#from word_values import sort_by_letter_frequency


class Browser():
    def __init__(self, url):
        self.url = url
        self._initiate_browser()

    
    def _expand_shadow_element(self, element):
        """
        expanding shadow root elements to allow access to the selenium webdriver
        element: which element to expand 
        """
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root

    def _initiate_browser(self):
        """
        method to initiate the webdriver, and direct to the webpage
        """
        self.browser = webdriver.Safari()
        self.browser.get(self.url)
        return self

    
    def select_item(self, element_name: str, element_type: By):
        """
        element_name: name of the element to write to 
        element_type: type of element to write to: i.e: By.CLASS, By.ID...
        ---
        Method to select / click an item on the page
        """
        item = self.browser.find_element(element_type, element_name)
        return item
    
    def input_text(self, element_name: str, element_type: By, word: str):
        """
        element_name: name of the element to write to 
        element_type: type of element to write to: i.e: By.CLASS, By.ID...
        word: word to input to the element
        ---
        method to write into an input on the webpage
        """
        item = self.browser.find_element(element_type, element_name)
        item.send_keys(word)
        item.send_keys(Keys.RETURN)

        return self


    
    def delete_text(self, element_name: str, element_type: By, length: int):
        """
        element_name: name of the element to write to 
        element_type: type of element to write to: i.e: class, id...
        length: length of the string to delete
        ---
        method to delete an input for a given element on the webpage
        """
        item = self.browser.find_element(element_type, element_name)
        for _ in range(length):
            item.send_keys(Keys.BACKSPACE)

        return self


if __name__ == '__main__':
    pass