# Wikipedia scraping | Highschools in the USA

## Description of the project

The whole idea of this great project is to get a list of all high schools in the United States. For this reason, we had to use the most trustworthy and yet free source of information we could find, which in this case was Wikipedea.com, which was a really hard task considering that there was a separate website for each of the 50 states in the US, where most of them were pretty similar to each other but almost a half were different from each other which led to the need of creating new algorithms for many pages. Finally, the information retrieved had to be stored both in an Excel sheet and in a JSON file.

## Process of scraping

First of all the program exctracted a list of the URLs of the High Schools in each state in the USA with the **get_state_urls()** function, which returns the list of all the states and is passed as an argument to the **get_schools()** function. This function retrieves the *name, county and city* of each school in each of the states whose page structure is similar, if not the case this function calls the proper **Special function** of the state. the information retrieved gets cleaned of certain patterns (like words inside the parenthesis or square brackets) by using regular expresions to find them and erase them.

Once the information is retrieved, **SaveData()** function is in charge of exporting the output to an Excel Sheet and JSON file. 

## Technologies I used

+ Python Programming language.
+ JSON library.
+ BeautifulSoup library.
+ Regular Expressions.
+ Pandas library.
+ Requests library.
+ Microsoft Excel.
