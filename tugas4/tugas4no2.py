from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import sys
from bs4 import BeautifulSoup

url = "https://nim-lang.org/docs/lib.html"

webdriver = webdriver.Firefox(executable_path=GeckoDriverManager().install())


def getNimDoc(search_query, number):
    wait = WebDriverWait(webdriver, 2)
    webdriver.get(url)

    search = webdriver.find_element_by_id("searchInput")
    search.send_keys(search_query + Keys.RETURN)

    sleep(2)

    page = webdriver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    filter1 = soup.find_all('div', class_='nine columns')
    filter2 = filter1[0]
    filter3 = filter2.find_all('div', class_='search_results')
    filter4 = filter3[0]
    filter5 = filter4.find_all('li')
    
    n=1    
    for i in filter5:
        if n <= number:
            get_title = i.a.text
            get_url = i.find('a').get('href')
            print(n, "Title = ", get_title, '\n',"Url = ", get_url,'\n')
            print("-------------------------------------------------------------------------------------------------")
            n+=1
        else: break

query1 = str(input("Query: "))
number = int(input("Jumlah: "))        
getNimDoc(query1, number)
