from this import s
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
            pass
            #all_schools.append(missouri(url, 'Missouri'))

        elif state_name == 'South Dakota':
            pass

            #all_schools.append(south_dakota(url))

        elif state_name == 'Delaware':
            pass
            
            #all_schools.append(delaware(url))

        elif state_name == 'New Hampshire':
            pass
            
            #all_schools.append(new_hampshire(url))
            
        elif state_name == 'Connecticut':
            pass
            
            #all_schools.append(connecticut(url))
            
        elif state_name == 'Oregon':
            pass
            
            #all_schools.append(oregon(url))

        elif state_name == 'Indiana':
            pass
            
            #all_schools.append(indiana(url))

        elif state_name == 'Alaska':
            pass
            
            #all_schools.append(diff_states(url, 'Alaska'))
            
        elif state_name == 'Wyoming':
            pass
                
            #all_schools.append(diff_states(url, 'Wyoming'))

        #elif state_name == 'Massachusetts':
         #   pass
    
        elif state_name == 'Pennsylvania':

            counties = soup.find_all('h2')

            for county in counties:

                if 'County' not in county.text and 'Ward' not in county.text and 'City' not in county.text:

                    pass

                elif state_name == 'Idaho':
                    
                    print('*'*50, 'You are in Idaho', '*'*50)

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
                                    city = school_info[1]

                                    school_output = {
                                        'School name': name, 
                                        'State': state_name,
                                        'County/Wars': county,
                                        'City/town/village/District': city,
                                    }

                                    all_schools.append(school_output)

                                    print(school_output)

                                    time.sleep(0.001)

                        elif next_element.name == 'h3':
                            print('next element: ', next_element.name)

                            county = next_element.text

                            time.sleep(0.001)

                        elif next_element.name == 'h2':
                            break

                        else:
                            pass

                        next_element = next_element.find_next_sibling()

                else:

                    print('*'*50, county.text, '*'*50)

                    time.sleep(0.001)

                    next_element = county.find_next_sibling()

                    city = ''

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

                                    if ', ' in school:

                                        school_info = school.split(', ')

                                        if school_info > 2:

                                            name == ''
                                            for school_splited_name in school_info[0:len(school_info)-1]:

                                                name += school_splited_name.text 

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


#check Massachusetts and New Jersey and North Dakota and Utah (problems with ' - ')

def new_jersey(url):

    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    time.sleep(0.001)

    counties = soup.find_all('h3')

    output = []

    for county in counties:

        if 'County' not in county.text:
            pass

        else:

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
                            city = school_info[1]

                            school_output = {
                            'School name': name, 
                            'State': 'New Jersey',
                            'County/Wars': county.text.replace('[edit]',''),
                            'City/town/village/District': city,
                            }

                            output.append(school_output)

                            print(school_output)

                            time.sleep(0.001)

                        else:

                            school_output = {
                            'School name': school, 
                            'State': 'New Jersey',
                            'County/Ward': county.text.replace('[edit]',''),
                            'City/town/village/District': 'Not specified',
                            }

                            output.append(school_output)

                            print(school_output)

                            time.sleep(0.001)

                elif next_element.name == 'h3':
                    break

                else:
                    pass

                next_element = next_element.find_next_sibling()

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
        'County/Ward/District': info[3].text,
        'City/town/village': info[2].text
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
                'County/Ward/District': county.text.replace('[edit]', ''),
                'City/town/village': info[1].text
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
            'County/Ward/District': info[2].text.replace('\n', ''),
            'City/town/village': info[1].text.replace('\n', '')
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
            'County/Ward/District': info[3].text,
            'City/town/village': info[2].text
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
            'County/Ward/District': 'Not specified',
            'City/town/village': info[2].text
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
                    'County/Ward/District': county.text.replace('[edit]', ''),
                    'City/town/village': info[1].text
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

    df = pd.DataFrame(OP, columns=['School name', 'State', 'County', 'City/town/village'])
    df.to_excel('High Schools in the USA.xls', index=True, columns=['School name', 'State', 'County/Ward', 'City/town/village/District'])



new_jersey('https://en.wikipedia.org/wiki/List_of_high_schools_in_New_Jersey')

#get_schools(get_state_urls(parent_url))