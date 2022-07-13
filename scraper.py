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

    cleaning_pattern = r'-.{20,}|\(.*\)|\[.*\]'

    key_words = ['Public', 'Private', 'ern', 'Central', 'Neighborhood', 'Admission', 'Charter', 'Defunc'] 

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

        if state_name == 'Missouri':
            missouri(url)
            pass

        for county in counties:

            if 'County' not in county.text and 'Ward' not in county.text:

                pass

            elif 'Schools' in county.text:
                
                print('*'*50, 'You are in Idaho', '*'*50)

                time.sleep(0.05)

                next_element = county.find_next_sibling()

                while True:

                    if next_element.name == 'div' or next_element.name == 'ul':

                        print('next element: ', next_element.name)

                        time.sleep(0.05)

                        school_list = next_element.find_all('li')
                        schools = [school.text for school in school_list]

                        for school in schools:

                            if ', ' in school:

                                school_info = school.split(', ')
                                name = school_info[0]
                                city = school_info[1]

                                school_output = {
                                    'School name': name, 
                                    'State': state_name,
                                    'County': county,
                                    'City/town/village/District': city,
                                }

                                all_schools.append(school_output)

                                print(school_output)

                                time.sleep(0.05)

                    elif next_element.name == 'h3':
                        print('next element: ', next_element.name)

                        county = next_element.text

                        time.sleep(0.05)

                    elif next_element.name == 'h2':
                        break

                    else:
                        pass

                    next_element = next_element.find_next_sibling()

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

                        schools = []

                        for school_list_child in school_list:
                            
                            if school_list_child.find('ul'):

                                school_list_child = school_list_child.find_all('li')

                                for schools_in_slc in school_list_child:
                                    
                                    if schools_in_slc.find('ul'):

                                        school_in_slc = school_in_slc.find_all('li')

                                        for school_in_slcc in school_list_child:

                                            school = school_in_slcc.text
                                            schools.append(school)
                                    else:

                                        school = school_in_slc.text
                                        schools.append(school)
                            else:

                                school = school_list_child.text
                                schools.append(school)

                            time.sleep(0.01)

                        for school in schools:

                            if ', ' in school:

                                school = re.sub(cleaning_pattern, '', school)

                                school_info = school.split(', ')
                                name = school_info[0]
                                city = school_info[1]

                                school_output = {
                                    'School name': name, 
                                    'State': state_name,
                                    'County/Ward': county.text,
                                    'City/town/village/District': city,
                                }

                                all_schools.append(school_output)

                                print(school_output)

                                time.sleep(0.05)

                            elif city:

                                school = re.sub(cleaning_pattern, '', school)

                                school_output = {
                                    'School name': school, 
                                    'State': state_name,
                                    'County/Ward': county.text,
                                    'City/town/village/District': city,
                                }

                                all_schools.append(school_output)

                                print(school_output)

                                time.sleep(0.05)

                    elif next_element.name == 'h3':
                        print('next element: ', next_element.name)

                        ne = next_element.text

                        if any(kw in ne for kw in key_words):

                            print('Not a city or district - Not valid h3 element')

                            pass

                        else:
                            city = next_element.text

                        time.sleep(0.05)

                    elif next_element.name == 'h2':
                        break

                    else:
                        pass

                    next_element = next_element.find_next_sibling()

    return all_schools


def missouri(url):
    pass

def south_dakota(url):
    
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    items = soup.find_all('tr')

    output = []

    for item in items:

        info = item.find_all('td')

        school_output = {
        'School name': info[0].text, 
        'State': 'South Dakota',
        'County/Ward/District': info[3].text,
        'City/town/village': info[2].text
        }

        output.append(school_output)

    return output


def delaware(url):
    
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    counties = soup.find_all('h3')

    output = []

    for county in counties:

        if 'County' in county.text:

            table = county.find_next_element()

            items = table.find_all('tr')

            for item in items:

                info = item.find_all('td')

                school_output = {
                'School name': info[0].text, 
                'State': 'Delaware',
                'County/Ward/District': county.text,
                'City/town/village': info[1].text
                }

                output.append(school_output)

        else:
            pass

    return output

def new_hampshire(url):
    
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    items = soup.find_all('tr')

    output = []

    for item in items:

        info = item.find_all('td')

        school_output = {
        'School name': info[0].text, 
        'State': 'New Hampshire',
        'County/Ward/District': info[2].text,
        'City/town/village': info[1].text
        }

        output.append(school_output)

    return output

def connecticut(url):
    
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    items = soup.find_all('tr')

    output = []

    for item in items:

        info = item.find_all('td')

        school_output = {
        'School name': info[0].text, 
        'State': 'Connecticut',
        'County/Ward/District': info[3].text,
        'City/town/village': info[2].text
        }

        output.append(school_output)

    return output

def oregon(url):

    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    items = soup.find_all('tr')

    output = []

    for item in items:

        info = item.find_all('td')

        school_output = {
        'School name': info[1].text, 
        'State': 'Oregon',
        'County/Ward/District': info[2].text,
        'City/town/village': 'Not specified'
        }

        output.append(school_output)

    return output

def indiana(url):

    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    counties = soup.find_all('h3')

    output = []

    for county in counties:

        if 'County' in county.text:

            table = county.find_next_element()

            items = table.find_all('tr')

            for item in items:

                info = item.find_all('td')

                school_output = {
                'School name': info[0].text, 
                'State': 'Indiana',
                'County/Ward/District': county.text,
                'City/town/village': info[1].text
                }

                output.append(school_output)

        else:
            pass

    return output


def diff_states(url):

    output = []

    cleaning_pattern = r'-.{20,}|\(.*\)|\[.*\]'

    key_words = ['Public', 'Private', 'ern', 'Central', 'Neighborhood', 'Admission', 'Charter', 'Defunc'] 

    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    counties = soup.find_all('h2')

    for county in counties:

        if 'County' not in county.text and 'Ward' not in county.text:

            pass

        elif 'Schools' in county.text:
                
            print('*'*50, 'You are in Idaho', '*'*50)

            time.sleep(0.05)

            next_element = county.find_next_sibling()

            while True:

                if next_element.name == 'div' or next_element.name == 'ul':

                    print('next element: ', next_element.name)

                    time.sleep(0.05)

                    school_list = next_element.find_all('li')
                    schools = [school.text for school in school_list]

                    for school in schools:

                        if ', ' in school:

                            school_info = school.split(', ')
                            name = school_info[0]
                            city = school_info[1]

                            school_output = {
                                'School name': name, 
                                'State': state_name,
                                'County': county,
                                'City/town/village/District': city,
                            }

                            all_schools.append(school_output)

                            print(school_output)

                            time.sleep(0.05)

                elif next_element.name == 'h3':
                    print('next element: ', next_element.name)

                    county = next_element.text

                    time.sleep(0.05)

                elif next_element.name == 'h2':
                    break

                else:
                    pass

                next_element = next_element.find_next_sibling()

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

                    schools = []

                    for school_list_child in school_list:
                            
                        if school_list_child.find('ul'):

                            school_list_child = school_list_child.find_all('li')

                            for schools_in_slc in school_list_child:
                                    
                                if schools_in_slc.find('ul'):
                                    
                                    school_in_slc = school_in_slc.find_all('li')

                                    for school_in_slcc in school_list_child:

                                        school = school_in_slcc.text
                                        schools.append(school)
                                else:

                                    school = school_in_slc.text
                                    schools.append(school)
                        else:

                            school = school_list_child.text
                            schools.append(school)

                        time.sleep(0.01)

                    for school in schools:

                        if ', ' in school:

                           school = re.sub(cleaning_pattern, '', school)

                            school_info = school.split(', ')
                            name = school_info[0]
                            city = school_info[1]

                            school_output = {
                                'School name': name, 
                                'State': state_name,
                                'County/Ward': county.text,
                                'City/town/village/District': city,
                            }

                            all_schools.append(school_output)

                            print(school_output)

                            time.sleep(0.05)

                        elif city:

                            school = re.sub(cleaning_pattern, '', school)

                            school_output = {
                                'School name': school, 
                                'State': state_name,
                                'County/Ward': county.text,
                                'City/town/village/District': city,
                            }

                            all_schools.append(school_output)

                            print(school_output)

                            time.sleep(0.05)

                elif next_element.name == 'h3':
                    print('next element: ', next_element.name)

                    ne = next_element.text

                    if any(kw in ne for kw in key_words):

                        print('Not a city or district - Not valid h3 element')
                        pass

                    else:
                        city = next_element.text

                    time.sleep(0.05)

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

