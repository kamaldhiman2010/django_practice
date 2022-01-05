import requests
from bs4 import BeautifulSoup
# from requests.sessions import session
from requests_html import HTMLSession
from csv import writer
session= HTMLSession()
url="https://www.pararius.com/apartments/amsterdam?ac=1"
page=session.get(url)

soup=BeautifulSoup(page.content,'html.parser')
# print(soup.prettify())
lists=soup.find_all('section',class_="listing-search-item")
with open('housing.csv','w',encoding='utf-8',newline='') as f:
    thewriter = writer(f)
    header=['Title','Location','Price','Area']
    thewriter.writerow(header)
    for l in lists:
        title=l.find('a',class_="listing-search-item__link--title").text.replace('\n','')
        location=l.find('div',class_="listing-search-item__location").text.replace('\n','')
        price=l.find('div',class_="listing-search-item__price").text.replace('\n','')
        area=l.find('li',class_="illustrated-features__item illustrated-features__item--surface-area").text.replace('\n','')
        info=[title,location,price,area]
        thewriter.writerow(info)
        print(info)