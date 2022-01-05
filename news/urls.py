from os import name
from django.contrib import admin
from . import views
from django.conf import settings
from django.urls import path, include, reverse
from django.conf.urls.static import static

urlpatterns = [
   
    path('news/',views.index,name='index'),
 
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)