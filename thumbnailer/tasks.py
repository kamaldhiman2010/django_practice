from celery import shared_task

import os
from zipfile import ZipFile

from PIL import Image
from .models import AllUser,Adult,Aged,Children

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

@shared_task
def adding_task(x, y):
    return x + y


@shared_task
def make_thumbnails(file_path, thumbnails=[]):
    os.chdir(settings.IMAGES_DIR)
    path, file = os.path.split(file_path)
    file_name, ext = os.path.splitext(file)

    zip_file = f"{file_name}.zip"
    results = {'archive_path': f"{settings.MEDIA_URL}images/{zip_file}"}
    try:
        img = Image.open(file_path)
        zipper = ZipFile(zip_file, 'w')
        zipper.write(file)
        os.remove(file_path)
        for w, h in thumbnails:
            img_copy = img.copy()
            img_copy.thumbnail((w, h))
            thumbnail_file = f'{file_name}_{w}x{h}.{ext}'
            img_copy.save(thumbnail_file)
            zipper.write(thumbnail_file)
            os.remove(thumbnail_file)

        img.close()
        zipper.close()
    except IOError as e:
        print(e)

    return results

from time import sleep
@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def send_email_task(*args,**kwargs):
    sleep(10)
    send_mail('celery task worked!',
    'This is proof the task worked!',
    'kamaldhiman2010@gmail.com',
    ['kkuljit2010@gmail.com','kamaldhiman2010@gmail.com'])

    return None



@shared_task
def create_profile(instance):
    created=AllUser.objects.get(id=instance.id)
    if created:
        age=instance.age
        age=int(age)
        if age<18:
            Children.objects.create(name=instance,age=instance.age,first_name=instance.first_name,last_name=instance.last_name,email=instance.email,password=instance.password)
            print("child created")
        elif age>=18 or age<=50:
            Adult.objects.create(name=instance,age=instance.age,first_name=instance.first_name,last_name=instance.last_name,email=instance.email,password=instance.password)
            print("adult created")
        elif age>50:
            Aged.objects.create(name=instance,age=instance.age,first_name=instance.first_name,last_name=instance.last_name,email=instance.email,password=instance.password)
            print("aged")
        else:
            print('fdjnvj')
       
        print("profile created")



@shared_task
def update_profile(instance):
    created=AllUser.objects.filter(id=instance.id).update(username=instance.username,age=instance.age,first_name=instance.first_name,last_name=instance.last_name,email=instance.email,password=instance.password)
    if not created:
        current_obj=instance
        print(current_obj)
        age=instance.age
        age=int(age)
        if age<18:
            
            data = Children.objects.filter(name_id=instance.id)
            if data:
                instance.data_set.update(name=instance,age=instance.age,first_name=instance.first_name,last_name=instance.last_name,email=instance.email,password=instance.password)
                # child=data.alluser_set.all()
                # if child.age<18:
                #     data.update(name=instance,age=instance.age,first_name=instance.first_name,last_name=instance.last_name,email=instance.email,password=instance.password)
                # else:
                #     child.delete()
            # else:
            #     Children.objects.create(name=instance,age=instance.age,first_name=instance.first_name,last_name=instance.last_name,email=instance.email,password=instance.password)
                
        elif age>=18 & age<=50:
            data=Adult.objects.filter(name_id=instance.id)
            if data:
                data.update(name=instance,age=instance.age,first_name=instance.first_name,last_name=instance.last_name,email=instance.email,password=instance.password)
            else:
                Adult.objects.create(name=instance,age=instance.age,first_name=instance.first_name,last_name=instance.last_name,email=instance.email,password=instance.password)

        elif age>50:
            data=Aged.objects.filter(name_id=instance.id)
            if data:
                data.update(name=instance,age=instance.age,first_name=instance.first_name,last_name=instance.last_name,email=instance.email,password=instance.password)
            else:
                Aged.objects.create(name=instance,age=instance.age,first_name=instance.first_name,last_name=instance.last_name,email=instance.email,password=instance.password)


        # Adult.objects.filter(name=instance).update()
        print("updated profile")



    
    


