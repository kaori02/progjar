import requests
from bs4 import BeautifulSoup

urls = []
titles = []

def getGoPackage(query, n):
    global pages

    if n <= 10 :
        pages = 1
    elif n <= 20 :
        pages = 2
    elif n <= 30 :
        pages = 3
    elif n <= 40 :
        pages = 4
    elif n <= 50 :
        pages = 5
    elif n <= 60 :
        pages = 6
    else : 
        print("Invalid input")

    for page in range(pages):
        page = requests.get("https://pkg.go.dev/search?page=" + str(page) + "&q=" + query)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        filter1 = soup.find_all('div', class_ = 'LegacySearchSnippet')
        
        for container in filter1:
            get_url = container.h2.a.text.strip()
            get_url = get_url.replace('\n',"")
            urls.append(get_url)


            get_title = container.p.text
            titles.append(get_title)

query1 = str(input("Query: "))
number = int(input("Jumlah: "))        
getGoPackage(query1, number)
    

n=1
for i,j in zip(titles, urls):
    while n <= number :
        print(n, "Title = ", i, '\n',"Url = ", j,'\n')
        print("-------------------------------------------------------------------------------------------------")
        n+=1



            
            
        
        
        
        
