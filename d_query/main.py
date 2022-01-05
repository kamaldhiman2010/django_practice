# step 0: install libraries
# 1 pip install BeautifulSoup4
# 2 pip install requests
# 3 pip install html5lib

from bs4 import BeautifulSoup
import requests

# step 1: get the html

url="https://www.codewithharry.com/"
r=requests.get(url)
htmlcontent=r.content
# print(htmlcontent)

# step 3: Parse the html

soup=BeautifulSoup(htmlcontent, 'html.parser')
# print(soup.prettify())
# step 3:HTML tree traversal
title=soup.title #get the title of html page
# print(type(title)) # tag 
# print(type(title.string)) #navigable string
# print(type(soup)) #beautiful soup
# comment
# markup="<p><!-- comment --!></p>"
# soup2=BeautifulSoup(markup)
# print(type(soup2.p.string))

#get all the paragraphs from the page
paras=soup.find_all('p')
# print(paras)


# print(soup.find('p')) # get first element in the html page

# get classes of any element in the html page
# print(soup.find('p')['class'])

# find all the elements with class lead
# print(soup.find_all("p",class_="lead"))

#get the text from the tags/soup
# print(soup.find('p').get_text())


#get all text of page
# print(soup.get_text())


#get all the anchor tags from the page
anchors=soup.find_all('a')
# print(anchors)
all_links=set()
for link in anchors:
    if (link.get('href') != '#'):
        linktext="https://codewithharry.com"+link.get('href')
        all_links.add(linktext)
        # print(linktext)

navbarSupportedContent= soup.find(id='navbarSupportedContent')

#.contents = A tag's children are available as a list. it took memory when used
# .children = A tag's children are available as a generator.its not taking any when used .faster then contents

# for elem in navbarSupportedContent.children:
#     print(elem)

# for elem in navbarSupportedContent.contents:
#     print(elem)

# for elem in navbarSupportedContent.strings:
#     print(elem)

# for elem in navbarSupportedContent.stripped_strings:
#     print(elem)

# print(navbarSupportedContent.parents)

# for elem in navbarSupportedContent.parents:
    # print(elem.name)

# print(navbarSupportedContent.next_sibling)
# print(navbarSupportedContent.previous_sibling.previous_sibling)


#css selector
# elem=soup.select('#loginModal')
# print(elem)

elem=soup.select('.modal-footer')
print(elem)