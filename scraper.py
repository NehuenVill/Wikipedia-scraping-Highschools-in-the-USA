from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import json
import re

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

    all_schools = []

    cleaning_pattern = r'- [a-z ]{20,10000},? [a-z ]*|\([a-z ]*\)'

    for url in states_urls:

        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')

        unuseful_links = soup.find_all('link')

        split_url = url.split('_')
        state_name = split_url[len(split_url) - 1]


        print('*'*50, state_name, '*'*50)

        for i in unuseful_links:

            i.decompose()

        counties = soup.find_all('h2')

        for county in counties:

            if 'County' not in county.text and 'Ward' not in county.text:

                pass

            else:

                print('*'*50, county.text, '*'*50)

                time.sleep(0.05)

                next_element = county.find_next_sibling()

                city = ''

                while True:

                    if next_element.name == 'div' or next_element.name == 'ul':

                        if next_element['class'][0] == 'hatnote navigation-not-searchable':

                            pass

                        print('next element: ', next_element.name)

                        time.sleep(0.05)

                        school_list = next_element.find_all('li')
                        schools = [school.text for school in school_list]

                        for school in schools:

                            if ' - ' in school:

                                school = re.sub(cleaning_pattern, '', school)

                            if ', ' in school:

                                school_info = school.split(', ')
                                name = school_info[0]
                                city = school_info[1]

                                school_output = {
                                    'School name': name, 
                                    'State': state_name,
                                    'County': county.text,
                                    'City/town/village/District': city,
                                }

                                all_schools.append(school_output)

                                print(school_output)

                                time.sleep(0.05)

                            elif city:

                                school_output = {
                                    'School name': school, 
                                    'State': state_name,
                                    'County': county.text,
                                    'City/town/village': city,
                                }

                                all_schools.append(school_output)

                                print(school_output)

                                time.sleep(0.05)

                    elif next_element.name == 'h3':
                        print('next element: ', next_element.name)

                        time.sleep(0.05)

                        city = next_element.text

                    elif next_element.name == 'h2':
                        break

                    else:
                        pass

                    next_element = next_element.find_next_sibling()

    return all_schools


def SaveData(OP):

    df = pd.DataFrame(OP, columns=['School name', 'State', 'County', 'City/town/village'])
    df.to_excel('High Schools in the USA.xls', index=True, columns=['School name', 'State', 'County', 'City/town/village'])


get_schools(get_state_urls(parent_url))

