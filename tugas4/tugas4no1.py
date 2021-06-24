import requests
from bs4 import BeautifulSoup

urls = []
titles = []

def getGoPackage(query, n):
    global pages

    pages = n/10
    halaman = (pages-1)*10
    if halaman > 0 :
        pages=int(pages)+1

    for page in range(pages):
        page = requests.get("https://pkg.go.dev/search?page=" + str(page+1) + "&q=" + query)
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
        print(n, "Title = ", i, '\n',"Url = ", j,'\n')
        print("-------------------------------------------------------------------------------------------------")
        n+=1
        if n==number+1:
            break
