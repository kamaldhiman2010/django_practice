from django.db import models

# Create your models here.

class Images(models.Model):
    image_title=models.CharField(max_length=50)
    images=models.ImageField(upload_to='images/',blank=True)


class News(models.Model):
    title=models.CharField(max_length=50)
    posted_time=models.TextField()
    content=models.TextField()
    image_field=models.ImageField(upload_to='images/',blank=True)
    
