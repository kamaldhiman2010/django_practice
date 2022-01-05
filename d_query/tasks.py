# import string

# from django.contrib.auth.models import User
# from django.utils.crypto import get_random_string
# from .models import Post
# from celery import shared_task


# @shared_task
# def create_random_user_accounts(total):
#     for i in range(total):
#         title = 'post_title_{}'.format(get_random_string(10, string.ascii_letters))
#         subject = 'post_subject{}'.format(title)
        
#         Post.objects.create(title=title,subject=subject)
#     return '{}  posts are created with success!'.format(total)
from celery import Celery

from celery import shared_task
import time
from django.forms import modelform_factory
from django.contrib.auth.models import User

from d_query.forms import ParentForm
# broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'
# app = Celery('tasks', backend='amqp', broker='amqp://')
@shared_task()
def add(x, y):
    return x + y

@shared_task
def run1():
    while True:
        print('run1')
        time.sleep(2)
        return "run1 completed"
    


@shared_task
def run2():
    while True:
        print('run2')
        time.sleep(2)
    return "run2 completed"




@shared_task()
def gen_prime(x):
    multiples = []
    results = []
    print(x)
    for i in range(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in range(i*i, x+1, i):
                multiples.append(j)
            print(x)
    return results



# @shared_task
# def parent_info(request):
#     parent_info=User.objects.filter(user_id=request.user.id)
#     if parent_info:

#         parent=User.objects.filter(user_id=request.user.id).values('username','password','email')
        
#     return parent


    



