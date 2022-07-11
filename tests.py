
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

    counties = soup.find_all('h2')

    

    for county in counties:

        if 'County' not in county.text:

            pass

        else:

            school_list = county.find_next_sibling('ul')
            schools = school_list.find_all('li')

            print('')

            print(county)

            print('')

            print(school_list)

            print('')


get_info2()

            