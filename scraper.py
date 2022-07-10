from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import json

# Global variables:

parent_url = 'https://en.wikipedia.org/wiki/Category:Lists_of_high_schools_in_the_United_States_by_state'
base_url = 'https://en.wikipedia.org/'
states_url_list = []


def get_state_urls(url):

    request = 
