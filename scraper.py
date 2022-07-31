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
            print(link)
            states_url_list.append(link)

    return states_url_list

def get_schools(states_urls):

    all_schools = []

    cleaning_pattern = r' -.{20,}|\(.*\)|\[.*\]'

    key_words = ['Public', 'Private', 'Western', 'Northern', 'Southern', 'Estern', 'Central', 'Neighborhood', 'Admission', 'Charter', 'Defunc'] 

    for url in states_urls:

        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')

        state_name = url.replace('https://en.wikipedia.org/wiki/List_of_high_schools_in_', '').replace('_(U.S._state)','').replace('_', ' ')

        print('*'*50, state_name, '*'*50)

        if state_name == 'Missouri':
            
            data_scraped = missouri(url, 'Missouri')

            for data in data_scraped:
                all_schools.append(data)

        elif state_name == 'South Dakota':
            
            data_scraped = south_dakota(url)

            for data in data_scraped:
                all_schools.append(data)

        elif state_name == 'Delaware':
            
            data_scraped = delaware(url)

            for data in data_scraped:
                all_schools.append(data)

        elif state_name == 'New Hampshire':
            
            data_scraped = new_hampshire(url)

            for data in data_scraped:
                all_schools.append(data)
            
        elif state_name == 'Connecticut':
            
            data_scraped = connecticut(url)

            for data in data_scraped:
                all_schools.append(data)
            
        elif state_name == 'Oregon':
            
            data_scraped = oregon(url)

            for data in data_scraped:
                all_schools.append(data)

        elif state_name == 'Indiana':
            
            data_scraped = indiana(url)

            for data in data_scraped:
                all_schools.append(data)

        elif state_name == 'Alaska':
            
            data_scraped = diff_states(url, 'Alaska')

            for data in data_scraped:
                all_schools.append(data)
            
        elif state_name == 'Wyoming':
                
            data_scraped = diff_states(url, 'Wyoming')

            for data in data_scraped:
                all_schools.append(data)

        elif state_name == 'New Jersey' or state_name == 'Idaho':

            data_scraped = new_jersey_idaho(url, state_name)

            for data in data_scraped:
                all_schools.append(data)

        elif state_name == 'North Dakota' or state_name == 'Utah':

            data_scraped = northd_and_utah(url, state_name)

            for data in data_scraped:
                all_schools.append(data)

        else:

            if state_name == 'New York':

                data_scraped = ny_city()

                for data in data_scraped:
                    all_schools.append(data)

            counties = soup.find_all('h2')

            for county in counties:

                if 'County' not in county.text and 'Ward' not in county.text and 'City' not in county.text:

                    pass

                else:

                    print('*'*50, county.text, '*'*50)

                    time.sleep(0.001)

                    next_element = county.find_next_sibling()

                    city = ''

                    while True:

                        if next_element.name == 'div' and county.text == 'Middlesex County[edit]' and state_name == 'Massachusetts':

                            print('next element: ', next_element.name)

                            time.sleep(0.001)

                            school_list = next_element.find('ul')

                            school_list_items = school_list.find_all('li')

                            schools = [school.text for school in school_list_items]

                            for school in schools:

                                school = re.sub(cleaning_pattern, '', school)

                                if ', ' in school:

                                    school_info = school.split(', ')

                                    if len(school_info) > 2:

                                        name = ''
                                        for school_splited_name in school_info[0:len(school_info)-1]:

                                            name += school_splited_name 

                                        school_output = {
                                            'School name': name, 
                                            'State': state_name,
                                            'County/Ward': county.text.replace('[edit]',''),
                                            'City/town/village/District': school_info[len(school_info)-1].replace('[edit]',''),
                                        }

                                        all_schools.append(school_output)

                                        print(school_output)

                                        time.sleep(0.001)

                                    else:
                                        name = school_info[0]

                                        school_output = {
                                        'School name': name, 
                                        'State': state_name,
                                        'County/Ward': county.text.replace('[edit]',''),
                                        'City/town/village/District': school_info[1].replace('[edit]',''),
                                        }

                                        all_schools.append(school_output)

                                        print(school_output)

                                        time.sleep(0.001)

                                else:

                                    school_output = {
                                    'School name': school, 
                                    'State': state_name,
                                    'County/Ward': county.text.replace('[edit]',''),
                                    'City/town/village/District': 'Not specified',
                                    }

                                    all_schools.append(school_output)

                                    print(school_output)

                                    time.sleep(0.001)

                            counties = next_element.find_all('h2')

                            for county in counties[0:5]:

                                print('*'*50, county.text, '*'*50)

                                time.sleep(0.001)

                                next_element = county.find_next_sibling()

                                while True:

                                    if next_element.name == 'div' or next_element.name == 'ul':

                                        print('next element: ', next_element.name)

                                        time.sleep(0.001)

                                        school_list = next_element.find_all('li')
                                        schools = [school.text for school in school_list]

                                        for school in schools:

                                            if ', ' in school:

                                                school_info = school.split(', ')
                                                name = school_info[0]

                                                school_output = {
                                                    'School name': name, 
                                                    'State': state_name,
                                                    'County/Ward': county.text.replace('[edit]', ''),
                                                    'City/town/village/District': school_info[1],
                                                }

                                                all_schools.append(school_output)

                                                print(school_output)

                                                time.sleep(0.001)

                                    elif next_element.name == 'h2':
                                        break

                                    else:
                                        pass

                                    next_element = next_element.find_next_sibling()
                            break

                        elif next_element.name == 'div' or next_element.name == 'ul':

                            try:

                                if next_element['class'][0] == 'hatnote navigation-not-searchable':
                                    pass

                                else:
                                    raise KeyError
                            
                            except KeyError:

                                print('next element: ', next_element.name)

                                time.sleep(0.001)

                                school_list = next_element.find_all('li')

                                schools = [school.text for school in school_list]

                                parsed_schools = []

                                for school in schools:
                                    
                                    school_info = school.split('\n')

                                    if len(school_info) > 1:

                                        print('''
                                        
                                        
                                        An error ocurred.
                                        
                                        
                                        ''', school_info, '''
                                        
                                        
                                        
                                        
                                        ''')

                                        pass

                                    else:

                                        school = school_info[0]
                                        parsed_schools.append(school)


                                    time.sleep(0.001)

                                for school in parsed_schools:

                                    if state_name == 'Montana' or state_name == 'Kansas':
                                        
                                        school = re.sub(r' \(.*\)', '', school)

                                        school_info = school.split(', ')

                                        school_output = {
                                        'School name': school_info[0], 
                                        'State': state_name,
                                        'County/Ward': county.text.replace('[edit]',''),
                                        'City/town/village/District': school_info[1].replace('[edit]',''),
                                        }

                                        all_schools.append(school_output)

                                        print(school_output)

                                        time.sleep(0.001)

                                    else:

                                        school = re.sub(cleaning_pattern, '', school)

                                        if ', ' in school:

                                            school_info = school.split(', ')

                                            if len(school_info) > 2:

                                                name = ''
                                                for school_splited_name in school_info[0:len(school_info)-1]:

                                                    name += school_splited_name 

                                                school_output = {
                                                    'School name': name, 
                                                    'State': state_name,
                                                    'County/Ward': county.text.replace('[edit]',''),
                                                    'City/town/village/District': school_info[len(school_info)-1].replace('[edit]',''),
                                                }

                                                all_schools.append(school_output)

                                                print(school_output)

                                                time.sleep(0.001)

                                            else:
                                                name = school_info[0]

                                                school_output = {
                                                    'School name': name, 
                                                    'State': state_name,
                                                    'County/Ward': county.text.replace('[edit]',''),
                                                    'City/town/village/District': school_info[1].replace('[edit]',''),
                                                }

                                                all_schools.append(school_output)

                                                print(school_output)

                                                time.sleep(0.001)

                                        elif city:

                                            school_output = {
                                                'School name': school, 
                                                'State': state_name,
                                                'County/Ward': county.text.replace('[edit]',''),
                                                'City/town/village/District': city.replace('[edit]',''),
                                            }

                                            all_schools.append(school_output)

                                            print(school_output)

                                            time.sleep(0.001)

                                        else:

                                            school_output = {
                                                'School name': school, 
                                                'State': state_name,
                                                'County/Ward': county.text.replace('[edit]',''),
                                                'City/town/village/District': 'Not specified',
                                            }

                                            all_schools.append(school_output)

                                            print(school_output)

                                            time.sleep(0.001)

                        elif next_element.name == 'h3':
                            print('next element: ', next_element.name)

                            ne = next_element.text

                            if any(kw in ne for kw in key_words):

                                print('Not a city or district - Not valid h3 element')

                                pass

                            else:
                                city = next_element.text

                                print(city)

                            time.sleep(0.001)

                        elif next_element.name == 'h2':
                            break

                        else:
                            pass

                        next_element = next_element.find_next_sibling()

    return all_schools

# Special functions:

def ny_city():          #Works great
    
    req = requests.get('https://en.wikipedia.org/wiki/List_of_high_schools_in_New_York_City')
    soup = BeautifulSoup(req.text, 'html.parser')

    output = []

    cleaning_pattern = r'\n.*|\(.*\)'

    tables = soup.find_all('tbody')

    for i, table in enumerate(tables[0:5]):

        items = table.find_all('tr')

        for item in items[2:]:

            info = item.find_all('td')

            if i == 0:

                school_output = {
                    'School name': re.sub(cleaning_pattern, '', info[0].text),
                    'State': 'New York',
                    'County/Ward': 'The Bronx',
                    'City/town/village/District': 'New York City'
                    }

                print(school_output)

                output.append(school_output)

            elif i == 1:

                school_output = {
                    'School name': re.sub(cleaning_pattern, '', info[0].text), 
                    'State': 'New York',
                    'County/Ward': 'Brooklyn',
                    'City/town/village/District': 'New York City'
                    }

                print(school_output)

                output.append(school_output)

            elif i == 2:

                school_output = {
                    'School name': re.sub(cleaning_pattern, '', info[0].text),
                    'State': 'New York',
                    'County/Ward': 'Manhattan',
                    'City/town/village/District': 'New York City'
                    }

                print(school_output)

                output.append(school_output)

            elif i == 3:

                school_output = {
                    'School name': re.sub(cleaning_pattern, '', info[0].text),
                    'State': 'New York',
                    'County/Ward': 'Queens',
                    'City/town/village/District': 'New York City'
                    }

                print(school_output)

                output.append(school_output)

            elif i == 4:

                school_output = {
                    'School name': re.sub(cleaning_pattern, '', info[0].text), 
                    'State': 'New York',
                    'County/Ward': 'Staten Island',
                    'City/town/village/District': 'New York City'
                    }

                print(school_output)

                output.append(school_output)

    return output

def northd_and_utah(url, state_name):       #Works great

    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    cleaning_pattern = r'\(.*\)|\[.*\]'

    output = []

    counties = soup.find_all('h2')

    for county in counties:

        if 'County' not in county.text and 'Ward' not in county.text and 'City' not in county.text:

            pass

        else:

                    print('*'*50, county.text, '*'*50)

                    time.sleep(0.001)

                    next_element = county.find_next_sibling()

                    while True:

                        if next_element.name == 'div' or next_element.name == 'ul':

                            try:

                                if next_element['class'][0] == 'hatnote navigation-not-searchable':
                                    pass

                                else:
                                    raise KeyError
                            
                            except KeyError:

                                print('next element: ', next_element.name)

                                time.sleep(0.001)

                                school_list = next_element.find_all('li')

                                schools = [school.text for school in school_list]

                                parsed_schools = []

                                for school in schools:
                                    
                                    school_info = school.split('\n')

                                    if len(school_info) > 1:

                                        print('''
                                        
                                        
                                        An error ocurred.
                                        
                                        
                                        ''', school_info, '''
                                        
                                        
                                        
                                        
                                        ''')

                                        pass

                                    else:

                                        school = school_info[0]
                                        parsed_schools.append(school)


                                    time.sleep(0.001)

                                for school in parsed_schools:

                                    school = re.sub(cleaning_pattern, '', school)

                                    if ' - ' in school:

                                        school_info = school.split(' - ')

                                        if len(school_info) > 2:

                                            name = ''
                                            for school_splited_name in school_info[0:len(school_info)-1]:

                                                name += school_splited_name 

                                            school_output = {
                                                'School name': name, 
                                                'State': state_name,
                                                'County/Ward': county.text.replace('[edit]',''),
                                                'City/town/village/District': school_info[len(school_info)-1].replace('[edit]',''),
                                            }

                                            output.append(school_output)

                                            print(school_output)

                                            time.sleep(0.001)

                                        else:
                                            name = school_info[0]

                                            school_output = {
                                                'School name': name, 
                                                'State': state_name,
                                                'County/Ward': county.text.replace('[edit]',''),
                                                'City/town/village/District': school_info[1].replace('[edit]',''),
                                            }

                                            output.append(school_output)

                                            print(school_output)

                                            time.sleep(0.001)

                                    else:

                                        school_output = {
                                            'School name': school, 
                                            'State': state_name,
                                            'County/Ward': county.text.replace('[edit]',''),
                                            'City/town/village/District': 'Not specified',
                                        }

                                        output.append(school_output)

                                        print(school_output)

                                        time.sleep(0.001)

                        elif next_element.name == 'h2':
                            break

                        else:
                            pass

                        next_element = next_element.find_next_sibling()

    return output

def new_jersey_idaho(url, st_name):        #Works

    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    cleaning_pattern = r'\(.*\)|\[.*\]'

    counties = soup.find_all('h3')

    output = []

    for county in counties:

        if 'County' not in county.text and 'City' not in county.text:
            pass

        else:

            print('county: ', county.text, '*'*100)

            time.sleep(0.5)

            next_element = county.find_next_sibling()

            while True:

                if next_element.name == 'div' or next_element.name == 'ul':

                    print('next element: ', next_element.name)

                    time.sleep(0.001)

                    school_list = next_element.find_all('li')
                    schools = [school.text for school in school_list]

                    parsed_schools = []

                    for school in schools:
                                    
                        school_info = school.split('\n')

                        if len(school_info) > 1:

                            print('''
                                        
                                        
                                        An error ocurred.
                                        
                                        
                                        ''', school_info, '''
                                    
                                        
                                        
                                        
                                        ''')

                            pass

                        else:

                            school = school_info[0]
                            parsed_schools.append(school)


                            time.sleep(0.001)

                    for school in parsed_schools:

                            school = re.sub(cleaning_pattern, '', school)

                            if ', ' in school:

                                school_info = school.split(', ')

                                if len(school_info) > 2:

                                    name = ''
                                    for school_splited_name in school_info[0:len(school_info)-1]:

                                        name += school_splited_name 

                                    school_output = {
                                    'School name': name, 
                                    'State': st_name,
                                    'County/Ward': county.text.replace('[edit]',''),
                                    'City/town/village/District': school_info[len(school_info)-1].replace('[edit]',''),
                                    }

                                    output.append(school_output)

                                    print(school_output)

                                    time.sleep(0.001)

                                else:
                                    name = school_info[0]

                                    school_output = {
                                    'School name': name, 
                                    'State': st_name,
                                    'County/Ward': county.text.replace('[edit]',''),
                                    'City/town/village/District': school_info[1].replace('[edit]',''),
                                    }

                                    output.append(school_output)

                                    print(school_output)

                                    time.sleep(0.001)

                            else:

                                school_output = {
                                    'School name': school, 
                                    'State': st_name,
                                    'County/Ward': county.text.replace('[edit]',''),
                                    'City/town/village/District': 'Not specified',
                                }

                                output.append(school_output)

                                print(school_output)

                                time.sleep(0.001)


                elif next_element.name == 'h3' or next_element.name == 'h2':
                    break

                else:
                    pass

                next_element = next_element.find_next_sibling()

    return output

def missouri(url,state_name):   #Works

    output = []

    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    counties = soup.find_all('h2')

    for county in counties:

        if 'County' not in county.text:

            pass

        else:

            print('*'*50, county.text, '*'*50)

            time.sleep(0.001)

            next_element = county.find_next_sibling()

            city = ''

            while True:

                if next_element.name == 'ul':

                    print('next element: ', next_element.name)

                    time.sleep(0.001)

                    school_list = next_element.find_all('li')
                    schools = [school.text for school in school_list]
                    parsed_schools = []

                    for school in schools:
                            
                        print(school)
                        school_info = school.split('\n')

                        if len(school_info) > 1:

                            print('''
                                
                                
                            An error ocurred.
                                
                                
                            ''', school_info, '''
                                
                                
                                
                                
                            ''')

                            pass

                        else:
                            

                            school = school_info[0]
                            parsed_schools.append(school)
                            print(school)

                        time.sleep(0.001)

                    for school in parsed_schools:

                        school_output = {
                            'School name': school, 
                            'State': state_name,
                            'County/Ward': county.text.replace('[edit]',''),
                            'City/town/village/District': 'Not specified',
                        }

                        output.append(school_output)

                        print(school_output)

                        time.sleep(0.001)

                elif next_element.name == 'h2':
                    break

                else:
                    pass

                next_element = next_element.find_next_sibling()

    return output

def south_dakota(url):          #Works ok
    
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    table = soup.find('tbody')
    items = table.find_all('tr')

    output = []

    for item in items[1:]:

        info = item.find_all('td')

        print(info)

        school_output = {
        'School name': info[0].text, 
        'State': 'South Dakota',
        'County/Ward': info[3].text,
        'City/town/village/District': info[2].text
        }

        print(school_output)

        output.append(school_output)

    return output

def delaware(url):              #Works great
    
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    counties = soup.find_all('h3')

    output = []

    for county in counties:

        if 'County' in county.text:

            table = county.find_next_sibling()

            table_body = table.find('tbody')

            items = table_body.find_all('tr')

            for item in items[1:]:

                info = item.find_all('td')

                school_output = {
                'School name': info[0].text, 
                'State': 'Delaware',
                'County/Ward': county.text.replace('[edit]', ''),
                'City/town/village/District': info[1].text
                }

                print(school_output)

                output.append(school_output)

        else:
            pass

    return output

def new_hampshire(url):         #works great
    
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    items = soup.find_all('tr')

    output = []

    for item in items[1:]:
        try:
            info = item.find_all('td')

            school_output = {
            'School name': info[0].text.replace('\n', '') if '\n' in info[0].text else info[0].text, 
            'State': 'New Hampshire',
            'County/Ward': info[2].text.replace('\n', ''),
            'City/town/village/District': info[1].text.replace('\n', '')
            }

            print(school_output)

            output.append(school_output)
        except Exception:
            
            break

    return output

def connecticut(url):           #works great
    
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    items = soup.find_all('tr')

    output = []

    for item in items[1:]:
        try:
            info = item.find_all('td')

            school_output = {
            'School name': info[0].text, 
            'State': 'Connecticut',
            'County/Ward': info[3].text,
            'City/town/village/District': info[2].text
            }

            print(school_output)

            output.append(school_output)

        except:

            break

    return output

def oregon(url):                #works great

    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    items = soup.find_all('tr')

    output = []

    for item in items[2:]:

        try:

            info = item.find_all('td')

            school_output = {
            'School name': info[1].text, 
            'State': 'Oregon',
            'County/Ward': 'Not specified',
            'City/town/village/District': info[2].text
            }

            print(school_output)

            output.append(school_output)

        except Exception:

            break

    return output

def indiana(url):               #Works great

    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    counties = soup.find_all('h3')

    output = []

    for county in counties:

        if 'County' in county.text:

            table = county.find_next_sibling()

            print()

            table_body = table.find('tbody')

            items = table_body.find_all('tr')

            for item in items[1:]:

                try:

                    info = item.find_all('td')

                    school_output = {
                    'School name': info[0].text, 
                    'State': 'Indiana',
                    'County/Ward': county.text.replace('[edit]', ''),
                    'City/town/village/District': info[1].text
                    }

                    print(school_output)

                    output.append(school_output)

                except:

                    print('.............An error ocurred...........')
                    print(item)
                    pass
        else:
            pass

    return output

def diff_states(url, state_name):   #Works great

    output = []

    cleaning_pattern = r' -.{20,}|\(.*\)|\[.*\]'

    key_words = ['Public', 'Private', 'ern', 'Central', 'Neighborhood', 'Admission', 'Charter', 'Defunc'] 

    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    counties = soup.find_all('h2')

    for county in counties:

        if 'Borough' not in county.text and 'City' not in county.text and 'Municipality' not in county.text and 'Area' not in county.text and 'County' not in county.text:

            pass

        else:

            print('*'*50, county.text, '*'*50)

            time.sleep(0.001)

            next_element = county.find_next_sibling()

            city = ''

            while True:

                if next_element.name == 'ul':

                    print('next element: ', next_element.name)

                    time.sleep(0.001)

                    school_list = next_element.find_all('li')

                    schools = [school.text for school in school_list]

                    parsed_schools = []

                    for school in schools:
                            
                        school_info = school.split('\n')

                        if len(school_info) > 1:

                            print('''
                            
                            
                            An error ocurred.
                            
                            
                            ''', school_info, '''
                            
                            
                            
                            
                            ''')

                            pass

                        else:

                            school = school_info[0]
                            parsed_schools.append(school)


                        time.sleep(0.001)

                    for school in parsed_schools:

                        if ', ' in school:

                            school = re.sub(cleaning_pattern, '', school)
                            school_info = school.split(', ')
                            name = school_info[0]
                            city = school_info[1]

                            school_output = {
                                'School name': name, 
                                'State': state_name,
                                'County/Ward': county.text.replace('[edit]', ''),
                                'City/town/village/District': city,
                            }

                            output.append(school_output)

                            print(school_output)

                            time.sleep(0.001)

                elif next_element.name == 'table':
                    
                    print('next element: ', next_element.name)

                    table = next_element.find_all('tr')
                    
                    items = table[1:len(table)-1] if len(table) > 2 else table[1:]

                    for item in items:
                        
                        info = item.find_all('td')

                        school_output = {
                        'School name': info[0].text, 
                        'State': state_name,
                        'County/Ward': county.text.replace('[edit]',''),
                        'City/town/village/District': info[1].text
                        }

                        print(school_output)

                        output.append(school_output)


                elif next_element.name == 'h2':
                    break

                else:
                    print('next element: ', next_element.name)
                    pass

                next_element = next_element.find_next_sibling()

    return output

def SaveData(OP):

    with open('High_Schools_in_the_USA.json', 'w') as f:

        json.dump(OP, f)

    df = pd.DataFrame(OP, columns=['School name', 'State', 'County/Ward', 'City/town/village/District'])
    df.to_excel('High_Schools_in_the_USA.xls', index=True, columns=['School name', 'State', 'County/Ward', 'City/town/village/District'])



SaveData(get_schools(get_state_urls(parent_url)))