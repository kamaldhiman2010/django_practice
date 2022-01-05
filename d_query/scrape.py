from bs4 import BeautifulSoup
import requests
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from csv import writer
# driver = webdriver.Chrome(ChromeDriverManager().install())
url="https://www.pararius.com/apartments/amsterdam?ac=1"
# driver.get(url)
page=requests.get(url)
print(page.status_code)
soup=BeautifulSoup(page.content,'html.parser')
# page=driver.page_source
# soup=BeautifulSoup(page,'html.parser')
# print(soup.prettify())
info=[]
lists=soup.find_all('section',class_="listing-search-item")
print(lists)
# with open('housing.csv','w',encoding='utf-8',newline='') as f:s
#     thewriter=writer(f)
#     header=['Title','Location','Price','Area']
    # thewriter.writerow(header)
for list in lists:
    title=list.find('a',class_='listing-search-item__link--title').text.replace('\n','')
    location=list.find('div',class_='listing-search-item__location').text.replace('\n','')
    price=list.find('div',class_='listing-search-item__price').text.replace('\n','')
    area=list.find('li',class_='illustrated-features__item illustrated-features__item--surface-area').text.replace('\n','')
    info=[title,location,price,area]
    
    # thewriter.writerow(info)
    # print(info)