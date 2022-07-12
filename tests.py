
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import json

def get_info():

    req = requests.get('https://en.wikipedia.org/wiki/List_of_high_schools_in_Alabama')
    soup = BeautifulSoup(req.text, 'html.parser')

    counties = soup.find_all('h2')

    for county in counties:

        if 'County' not in county.text:

            pass

        else:

            try:

                school_list = county.find_next_sibling('ul')
                schools = school_list.find_all('li')

                for school in schools:

                    school_info = school.text

                    try:

                        info = school_info.split(', ')

                        name = info[0]
                        city = info[1]

                    except:
                            
                        name = school_info
                            
                    finally:
                            
                        school_output = {
                            'School name': name, 
                            'County': county.text,
                            'City/town/village': city
                        }

                        print(school_output)

                city = county.find_next_sibling('h3')

                while True:

                    school_list = city.find_next_sibling('ul')
                    schools = school_list.find_all('li')

                    for school in schools:

                        name = school.text
                        city_name = city.text
                            
                        school_output = {
                            'School name': name, 
                            'County': county.text,
                            'City/town/village': city_name
                        }

                        print(school_output)

                        if 'County' in school_list.next_sibling.text:
                            
                            break 

                        elif school_list.find_next_sibling('h3'):

                            city = school_list.find_next_sibling('h3')
                            
                        else:

                            break

            except:

                city = county.find_next_sibling('h3')

                while True:

                    school_list = city.find_next_sibling('ul')
                    schools = school_list.find_all('li')

                    for school in schools:

                        name = school.text
                        city_name = city.text
                            
                        school_output = {
                            'School name': name, 
                            'County': county.text,
                            'City/town/village': city_name
                        }

                        print(school_output)

                        if school_list.find_next_sibling('h3'):

                            city = school_list.find_next_sibling('h3')
                            
                        else:

                            break
                    
                    
                    
                            

#get_info()

def get_info2():

    req = requests.get('https://en.wikipedia.org/wiki/List_of_high_schools_in_Alabama')
    soup = BeautifulSoup(req.text, 'html.parser')

    unuseful_links = soup.find_all('link')

    for i in unuseful_links:

        i.decompose()

    counties = soup.find_all('h2')

    for county in counties:

        print('+'*20, county.text, '+'*20)

        if 'County' not in county.text:

            pass

        else:
            
            if county.find_next_sibling() == county.find_next_sibling('div'):

                print('+'*20 + 'if' + '+'*20)

                school_list_div = county.find_next_sibling('div')
                schools = school_list_div.find_all('li')

                for i in schools:

                    print(i)
                    print('')

            else:

                print('+'*20 + 'else' + '+'*20)

                school_list = county.find_next_sibling('ul')
                schools = school_list.find_all('li')

                for i in schools:

                    print(i)
                    print('')


#get_info2()


def get_info3():

    req = requests.get('https://en.wikipedia.org/wiki/List_of_high_schools_in_Alabama')
    soup = BeautifulSoup(req.text, 'html.parser')

    unuseful_links = soup.find_all('link')

    for i in unuseful_links:

        i.decompose()

    counties = soup.find_all('h2')

    for county in counties:

        if 'County' not in county.text:

            pass

        else:

            print("*"*50 + county.text + "*"*50)
            
            if county.find_next_sibling() == county.find_next_sibling('h3'):

                print('Case 1: h3 found -- ', county.text)

                city = county.find_next_sibling('h3')

                while True:

                    print('+'*20, city.text, '+'*20)

                    if city.find_next_sibling() == city.find_next_sibling('div'):

                        school_list_div = city.find_next_sibling('div')
                        schools = school_list_div.find_all('li')

                        for i in schools:

                            print(i)
                            print('')

                        if school_list_div.find_next_sibling() == school_list_div.find_next_sibling('h3'):
                            
                            city = school_list_div.find_next_sibling('h3')

                        elif school_list_div.find_next_sibling() == school_list_div.find_next_sibling('h2'):

                            break                            

                    elif city.find_next_sibling() == city.find_next_sibling('ul'):

                        school_list = city.find_next_sibling('div')
                        schools = school_list.find_all('li')

                        for i in schools:

                            print(i)
                            print('')

                        if school_list.find_next_sibling() == school_list.find_next_sibling('h3'):
                            
                            city = school_list.find_next_sibling('h3')

                        elif school_list.find_next_sibling() == school_list.find_next_sibling('h2'):

                            break     

            elif county.find_next_sibling() == county.find_next_sibling('div'):

                print('Case 2: div found -- ', county.text)

                school_list_div = county.find_next_sibling('div')
                schools = school_list_div.find_all('li')

                for i in schools:

                    print(i)
                    print('')

                if county.find_next_sibling() == county.find_next_sibling('h3'):

                    city = county.find_next_sibling('h3')

                    while True:

                        print('+'*20, city.text, '+'*20)

                        if city.find_next_sibling() == city.find_next_sibling('div'):

                            school_list_div = city.find_next_sibling('div')
                            schools = school_list_div.find_all('li')

                            for i in schools:

                                print(i)
                                print('')

                            if school_list_div.find_next_sibling() == school_list_div.find_next_sibling('h3'):
                                
                                city = school_list_div.find_next_sibling('h3')

                            elif school_list_div.find_next_sibling() == school_list_div.find_next_sibling('h2'):

                                break                            

                        elif city.find_next_sibling() == city.find_next_sibling('ul'):

                            school_list = city.find_next_sibling('div')
                            schools = school_list.find_all('li')

                            for i in schools:

                                print(i)
                                print('')

                            if school_list.find_next_sibling() == school_list.find_next_sibling('h3'):
                                
                                city = school_list.find_next_sibling('h3')

                            elif school_list.find_next_sibling() == school_list.find_next_sibling('h2'):

                                break
                    

            elif county.find_next_sibling() == county.find_next_sibling('ul'):

                print('Case 3: ul found -- ', county.text)

                school_list = county.find_next_sibling('ul')
                schools = school_list.find_all('li')

                for i in schools:

                    print(i)
                    print('')

                if county.find_next_sibling() == county.find_next_sibling('h3'):

                    city = county.find_next_sibling('h3')

                    while True:

                        print('+'*20, city.text, '+'*20)

                        if city.find_next_sibling() == city.find_next_sibling('div'):

                            school_list_div = city.find_next_sibling('div')
                            schools = school_list_div.find_all('li')

                            for i in schools:

                                print(i)
                                print('')

                            if school_list_div.find_next_sibling() == school_list_div.find_next_sibling('h3'):
                                
                                city = school_list_div.find_next_sibling('h3')

                            elif school_list_div.find_next_sibling() == school_list_div.find_next_sibling('h2'):

                                break                            

                        elif city.find_next_sibling() == city.find_next_sibling('ul'):

                            school_list = city.find_next_sibling('div')
                            schools = school_list.find_all('li')

                            for i in schools:

                                print(i)
                                print('')

                            if school_list.find_next_sibling() == school_list.find_next_sibling('h3'):
                                
                                city = school_list.find_next_sibling('h3')

                            elif school_list.find_next_sibling() == school_list.find_next_sibling('h2'):

                                break

#get_info3()

def get_info4():

    req = requests.get('https://en.wikipedia.org/wiki/List_of_high_schools_in_Alabama')
    soup = BeautifulSoup(req.text, 'html.parser')

    unuseful_links = soup.find_all('link')

    for i in unuseful_links:

        i.decompose()

    counties = soup.find_all('h2')

    for county in counties:

        if 'County' not in county.text:

            pass

        else:

            print('*'*50, county.text, '*'*50)

            time.sleep(0.5)

            next_element = county.find_next_sibling()

            city = ''
            school_type = ''

            while True:

                if next_element.name == 'div' or next_element.name == 'ul':

                    print('next element: ', next_element.name)

                    time.sleep(0.5)

                    school_list = next_element.find_all('li')
                    schools = [school.text for school in school_list]

                    for school in schools:

                        if ', ' in school:

                            school_info = school.split(', ')
                            name = school_info[0]
                            city = school_info[1]

                            school_output = {
                                'School name': name, 
                                'County': county.text,
                                'City/town/village': city,
                                'School type': 'Not specified'
                            }

                            print(school_output)

                            time.sleep(0.5)

                        elif school_type:
                            
                            school_output = {
                                'School name': school, 
                                'County': county.text,
                                'City/town/village': city,
                                'School type': school_type
                            }

                            print(school_output)

                            time.sleep(0.5)

                        elif city:

                            school_output = {
                                'School name': school, 
                                'County': county.text,
                                'City/town/village': city,
                                'School type': 'Not specified'
                            }

                            print(school_output)

                            time.sleep(0.5)

                elif next_element.name == 'h3':
                    print('next element: ', next_element.name)

                    time.sleep(0.5)

                    city = next_element.text

                elif next_element.name == 'h4':

                    print('next element: ', next_element.name)

                    time.sleep(0.5)

                    school_type = next_element.text

                elif next_element.name == 'h2':
                    break
                else:
                    pass

                next_element = next_element.find_next_sibling()
                

get_info4()
