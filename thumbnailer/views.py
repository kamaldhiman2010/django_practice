import os

from celery import current_app

from django import forms
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from thumbnailer.models import AllUser

from .tasks import create_profile, make_thumbnails, send_email_task

from django.http import HttpResponse


class FileUploadForm(forms.Form):
    image_file = forms.ImageField(required=True)


class HomeView(View):
    def get(self, request):
        form = FileUploadForm()
        return render(request, 'thumbnailer/home.html', {'form': form})

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        context = {}

        if form.is_valid():
            file_path = os.path.join(
                settings.IMAGES_DIR, request.FILES['image_file'].name)

            with open(file_path, 'wb+') as fp:
                for chunk in request.FILES['image_file']:
                    fp.write(chunk)

            task = make_thumbnails.delay(file_path, thumbnails=[(128, 128)])

            context['task_id'] = task.id
            context['task_status'] = task.status

            return render(request, 'thumbnailer/home.html', context)

        context['form'] = form

        return render(request, 'thumbnailer/home.html', context)


class TaskView(View):
    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()

        return JsonResponse(response_data)


def index(request):
    send_email_task.delay()
    return HttpResponse('Email sent successfully')


def all_users(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get('password')
        age = request.POST.get("age")
        print(age)
        alluser = AllUser.objects.create(
            username=username, first_name=first_name, last_name=last_name, email=email, password=password, age=age)
        print(alluser)

        print("sbhbjd")
        return HttpResponse("user is created")

    return render(request, 'thumbnailer/user.html',)
    # return redirect('all_users')
