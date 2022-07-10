from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import json

# Global variables:

parent_url = 'https://en.wikipedia.org/wiki/Category:Lists_of_high_schools_in_the_United_States_by_state'
base_url = 'https://en.wikipedia.org'

def get_state_urls(url):

    request = requests.get(parent_url)
    soup = BeautifulSoup(request.text, 'html.parser')

    state_lists = soup.find_all('div', class_ = 'mw-category-group')

    states_url_list = []

    for list in state_lists:

        states = list.find_all('a')

        for state in states:

            href = state['href']
            link = base_url + href

            states_url_list.append(link)

    return states_url_list


def get_schools(states_urls):

    for url in states_urls:

        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')

        

