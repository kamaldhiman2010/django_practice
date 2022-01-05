from django.db import models

# Create your models here.
class AllUser(models.Model):
    username=models.CharField(max_length=50,blank=True,null=True)
    first_name=models.CharField(max_length=50,blank=True,null=True)
    last_name=models.CharField(max_length=50,blank=True,null=True)
    email=models.EmailField(max_length=50,blank=True,null=True)
    password=models.CharField(max_length=50,blank=True,null=True)
    age=models.IntegerField()

    # def __str__(self):
    #     return self.username

class Children(models.Model):
    name=models.ForeignKey(AllUser,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50,blank=True,null=True)
    last_name=models.CharField(max_length=50,blank=True,null=True)
    email=models.EmailField(max_length=50,blank=True,null=True)
    password=models.CharField(max_length=50,blank=True,null=True)
    age=models.IntegerField(blank=True,null=True)

    # def __str__(self):
    #     return self.name


class Adult(models.Model):
    name=models.ForeignKey(AllUser,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    age=models.IntegerField()

    # def __str__(self):
    #     return self.name


class Aged(models.Model):
    name=models.ForeignKey(AllUser,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50,blank=True,null=True)
    last_name=models.CharField(max_length=50,blank=True,null=True)
    email=models.EmailField(max_length=50,blank=True,null=True)
    password=models.CharField(max_length=50,blank=True,null=True)
    age=models.IntegerField(blank=True,null=True)

    # def __str__(self):
    #     return self.name



