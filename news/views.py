from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.
from .models import News
import requests
from bs4 import BeautifulSoup



def index(request):
    url="https://www.ndtv.com/latest#pfrom=home-ndtv_mainnavgation"
    page=requests.get(url)
    soup=BeautifulSoup(page.content,"html.parser")
    ndtv_news=[]
    lists=soup.find_all(lambda tag: tag.name == 'div' and 
                                   tag.get('class') == ['news_Itm'])
    for l in lists:
       
        title=l.find('h2',class_='newsHdng').text
        posted_time=l.find('span',class_='posted-by').text

        content=l.find('p',class_='newsCont').text
        image_field=l.find('img')['src']

        # ndtv_news.append{title,posted_time,content,image_field))
        # print(ndtv_news)
        News.objects.get_or_create(title=title,posted_time=posted_time,content=content,image_field=image_field)
        # News.save()

        news_obj=News.objects.all()


    return render(request,'news.html',{'ndtv_news':news_obj})
