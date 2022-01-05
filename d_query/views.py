from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Permission
from django.http import HttpResponse, Http404, request
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from requests import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import reverse_lazy, reverse
from d_query.decorator import unauthenticated_user


from django_project import settings
from .forms import ParentForm, PaymentRegister, PostForm, LoginForm, UserRegisterForm, ResetPasswordForm
from .models import Payment, Post, NewsPaper, Comments, MultipleUsers
from .serializers import PostSerializer, UserSerializer, NewsPaperSerializer
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password, get_password_validators
from .tasks import *
from d_query.decorator import unauthenticated_user,allowed_users

import requests

# using simple register with forms.py
# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#
#             user_object = form.save()
#             login(request, user_object)
#             return redirect('login')
#         else:
#             print(form.errors)
#             return HttpResponse('ok')
#     else:
#         form = UserRegisterForm()
#         return render(request, 'register.html', {'form': form})


#   using make_password
from .templatetags.filter import PostFilter

from django.contrib.auth.decorators import permission_required



def register(request, account_activation_token=None):
    recent_user = User.objects.last()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user_object = form.save(commit=False)
            user_object.password = make_password(request.POST['password'])
            user_object.save()
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            messages.success(request, f"New account created: {username}")
            if user is not None:
                login(request, user)
                messages.success(request, 'you are now registered')

                recent_user = User.objects.get(id=recent_user.id)
                if recent_user.multipleusers.choice_field == 'S':
                    user_type = 'C'
                else:
                    user_type = 'S'
                MultipleUsers.objects.create(user=request.user, choice_field=user_type)
                # current_site = get_current_site(request)
                # message = render_to_string('acc_active_email.html', {
                #     'user': user, 'domain': current_site.domain,
                #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #     'token': account_activation_token.make_token(user),
                # })
                # Sending activation link in terminal
                # user.email_user(subject, message)
                # mail_subject = 'Activate your blog account.'
                # to_email = form.cleaned_data.get('email')
                # email = EmailMessage(mail_subject, message, to=[to_email])
                # email.send()
                # return HttpResponse('Please confirm your email address to complete the registration.')
                # subject = 'welcome to GFG world'
                # message = f'Hi {user.username}, thank you for registering in geeksforgeeks.'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [user.email, ]
                # send_mail(subject, message, email_from, recipient_list)

                # return redirect('post_list')
        else:
            print(form.errors)

            return redirect('login')
    else:
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})


@login_required(login_url='/login')
def set_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            print(request.POST)
            if request.POST["confirm_password"] == request.POST["new_password"]:
                print("----")
                if request.user.check_password(request.POST["password"]):
                    print("password")
                    user_obj = User.objects.get(id=request.user.id)
                    user_obj.password = make_password(request.POST["new_password"])
                    user_obj.save(commit=False)
                    print(user_obj)
                    return HttpResponse("password changed")
                return HttpResponse(" old password mismatched")
            return HttpResponse("password mistached")
        return HttpResponse("form invalid")

    else:
        form = ResetPasswordForm()
        return render(request, 'set_password.html', {'form': form})


def login_custom(request):
    # if not request.user.is_authenticated:
    #     return render(request, 'login_error.html')
    # print("view")
    # x=10/0

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'you are now logged in')
                # if request.user.multipleusers.choice_field == 'S':
                #     return redirect('post_list')
                # else:
                #     return redirect('all_posts')
                return redirect('post_list')
            else:
                messages.error(request, 'Invalid login credentials')
                return render(request, 'login.html', {'form': form})

    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout_custom(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')

def post_list(request):
  

        posts = Post.objects.filter(author_id=request.user.id).order_by('published_date')
        list_arr = [2, 4, 3, 1, 5, 7, 3, 12]
        addd=add.delay(1,8)
        run=run1()
        gen=gen_prime(200)
        print(gen)
        return render(request, 'blog.html', {'posts': posts, 'list_arr': list_arr,'addd':addd,'run':run1,'gen':gen})

def payment_register(request):
    profile = Payment.objects.filter(User_id=request.user.id)
    if request.method == 'POST':
        form = PaymentRegister(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            amount = form.cleaned_data.get('amount')
            invoiceid = form.cleaned_data.get('invoiceid')
            email = form.cleaned_data.get('email')
            return HttpResponse('success')
    else:
        form = PaymentRegister()
    return render(request, 'your_template.html', {'form':form})




# @permission_required('d_query.can_edit')
def all_posts(request):
   
    users = User.objects.all()
    
    # user=users.get(id=request.user.id)
    # if user.is_superuser:
    #     user.has_perm("d_query.can_edit")
    #     print(user)
    
    
    post = Post.objects.all()
    if request.method == 'POST':
        print(request.POST)
        if "search" and "user_id" in request.POST:
            search_term = request.POST['search']
            search_obj = Post.objects.filter(author_id=int(request.POST["user_id"])).filter(
                title__icontains=search_term)
            return render(request, 'all_posts.html',
                        {"post": search_obj, "user_id": int(request.POST["user_id"])})
        elif "search" in request.POST and not "user_id" in request.POST:
            search_term = request.POST['search']
            search_obj = Post.objects.filter(title__icontains=search_term)
            return render(request, 'all_posts.html',
                        {"post": search_obj, "users": users})
        else:
            post = Post.objects.filter(author_id=int(request.POST["user_id"])).order_by('published_date')
            return render(request, 'all_posts.html',
                        {"post": post, "users": users, "user_id": int(request.POST["user_id"])})
    return render(request, 'all_posts.html', {"post": post, "users": users})
    # return render(request, 'all_posts.html', {"users": users})

# def post_comment(request):
#     if request.method == 'POST':
        
#         company_form = PostForm(request.POST)
#         account_form = CommentForm(request.POST)

#         if company_form.is_valid() and account_form.is_valid():
            
#             company_form.save()
#             account_form.save()
#             return HttpResponseRedirect('/success')        

#         else:
#             context = {
#                 'company_form': company_form,
#                 'account_form': account_form,
#             }

#     else:
#         context = {
#         'company_form': PostForm(),
#         'account_form': CommentForm(),
#     }

#     return TemplateResponse(request, 'your_template.html', context)

def search(request):
    post_list = Post.objects.all()
    post_filter = PostFilter(request.GET, queryset=post_list)
    return render(request, 'post_list.html', {'filter': post_filter})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    return TemplateResponse(request, 'post_detail.html', {'post': post, 'name': 'Rahul'})



# def parent_info_new(request):
#     if request.method == 'POST':
#         form=parent_info()
#         if form.is_valid():
#             info=form.save(commit=False)
#             info.save()
#             return HttpResponse("success")
#     else:
#         form=ParentForm()
#         return render(request,'your_template.html',{"form":form})



def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "post added successfully")
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'post_edit.html', {'form': form})

# @permission_required("d_query.can_edit")
@login_required(login_url='/login')
def post_edit(request, pk):
    # if request.user.is_authenticated and request.user.has_perm('d_query.can_edit'):
    # permission = Permission.objects.get(name='can edit the post')
    # user = User.objects.get(id=request.user.id)
    # print(permission,user)
    # user.user_permissions.add(permission)
    # user.save()
    # if user.has_perm('d_query.can_edit'):
    post = Post.objects.get(pk=pk)
    if request.user == post.author or request.user.is_superuser:
    # post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                print("gjhgjh")
                post = form.save(commit=False)

                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'post_edit.html', {'form': form})
    return HttpResponse("you are not logged in ")



def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.delete()
    return redirect('post_list')

    # Post.objects.filter(pk=pk).delete()
    # return redirect('post_list')


def add_comments(request, id):
    user_obj = request.user
    print(user_obj.username)
    if user_obj.is_anonymous:
        user_obj = User.objects.get(id=1)
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        comments = request.POST.get("comment")
        Comments.objects.create(comments=comments, user=user_obj, post=post)

        return redirect('all_posts')
    else:
        return render(request, 'comments.html', {'post': post})


def new_detail(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        language = request.POST.get("language")
        post_ids = request.POST.getlist("post_ids")
        news_obj = NewsPaper.objects.create(name=name, language=language)
        if news_obj:
            for id in post_ids:
                post_obj = Post.objects.get(id=int(id))
                news_obj.post.add(post_obj)
            return redirect('new_posts')
    else:
        posts = Post.objects.all()

        return render(request, 'news.html', {'posts': posts})
    return redirect('new_detail')


def new_posts(request):
    news = NewsPaper.objects.all()
    return render(request, 'news_detail.html', {'news': news})


def news_edit(request, id):
    news = get_object_or_404(NewsPaper, id=id)
    if request.method == 'POST':
        news.post.clear()
        name = request.POST.get("name")
        language = request.POST.get("language")
        post_ids = request.POST.getlist("post_ids")
        print(post_ids)
        news_obj = NewsPaper.objects.filter(id=id).update(name=name, language=language)
        print(news_obj)
        if news_obj:

            for pid in post_ids:
                post_obj = Post.objects.get(id=int(pid))
                news.post.add(post_obj)
                print(news)
            return redirect('new_posts')


    else:
        posts = Post.objects.all()
        news_obj = NewsPaper.objects.get(id=id)
        post_list = list(news_obj.post.values_list('id', flat=True))
        return render(request, 'news.html', {'posts': posts, 'news': news_obj, 'post_list': post_list})
    return redirect('new_detail')


# class UserViewSet(viewsets.ModelViewSet):
#
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#
#
#
# class PostViewSet(viewsets.ModelViewSet):
#
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# def send_email():
#     email = EmailMessage(
#         'Title',
#         (UserSerializer.email),
#         'my-email',
#         ['my-receive-email']
#     )
#
#     email.send()

@api_view(['GET', 'POST'])
def user_listt(request):
    if request.method == 'GET':
        user_data = User.objects.all()
        serializer = UserSerializer(user_data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = User.objects.create_user(**request.data)
            subject = 'welcome to Django world'
            message = f'Hi {user_obj.username}, thank you for registering in django_project.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user_obj.email]
            send_mail(subject, message, email_from, recipient_list)
            # serializer.save()

            id = user_obj.id
            data = list(User.objects.filter(id=id).values('password', 'username'))
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth.hashers import make_password


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user_data = User.objects.get(pk=pk)

    except User.DoesNotExist:

        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        serializer = UserSerializer(user_data)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = UserSerializer(user_data, partial=True, data=request.data)
        if serializer.is_valid():
            if "password" in request.data:
                request.data['password'] = make_password(request.data['password'])
                print(request.data['password'])
            # serializer.save()
            user_obj = User.objects.filter(id=pk).update(**request.data)
            if user_obj:
                data = list(User.objects.filter(id=pk).values('password', 'username'))

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def post_listt(request):
    if request.method == 'GET':
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # User.objects.create_user(**request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def postt_detail(request, pk):
    try:

        post = Post.objects.get(pk=pk)

    except Post.DoesNotExist:

        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = PostSerializer(post, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def news_list(request):
    if request.method == 'GET':
        news_obj = NewsPaper.objects.all()
        serializer = NewsPaperSerializer(news_obj, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = NewsPaperSerializer(data=request.data)
        if serializer.is_valid():
            name = request.POST.get("name")
            language = request.POST.get("language")
            post_ids = request.POST.get("post")
            post_ids = post_ids.split(',')
            news_obj = NewsPaper.objects.create(name=name, language=language)
            if news_obj:
                for id in post_ids:
                    post_obj = Post.objects.get(id=int(id))
                    news_obj.post.add(post_obj)
            news_data = NewsPaper.objects.filter(id=news_obj.id).values()
            return Response(news_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def news_update(request, pk):
    try:
        newspaper = NewsPaper.objects.get(pk=pk)
    except NewsPaper.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = NewsPaperSerializer(newspaper)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = NewsPaperSerializer(newspaper, data=request.data, partial=True)
        if serializer.is_valid():

            newspaper.post.clear()
            name = request.POST.get("name")
            language = request.POST.get("language")
            post_ids = request.POST.get("post")
            post_ids = post_ids.split(',')
            print(post_ids)
            news_obj = NewsPaper.objects.filter(pk=pk).update(name=name, language=language)
            print(news_obj)
            if news_obj:

                for id in post_ids:
                    post_obj = Post.objects.get(id=int(id))
                    newspaper.post.add(post_obj)
            news_data = NewsPaper.objects.get(pk=pk)
            serializer = NewsPaperSerializer(news_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        newspaper.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCreateView(CreateView):
    model = Post
    fields = ('title', 'subject', 'images', 'video')
    template_name = 'post_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)
        # return reverse('post_list')


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'post'
    fields = ('title', 'subject', 'images', 'video')

    def get_success_url(self):
        return reverse_lazy('detail_post', kwargs={'pk': self.object.id})


class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'

    def get_queryset(self):
        print(self.request.user)
        if self.request.user is not None:
            print("gyjkgj,b")

            queryset = Post.objects.filter(author=self.request.user)

        return queryset


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog.html'


class NewsPaperView(ListView):
    model = NewsPaper
    template_name = 'news_detail.html'
    context_object_name = 'news'


class NewsPaperCreate(CreateView):
    model = NewsPaper
    template_name = 'news.html'
    fields = ('name', 'language', 'post')
    extra_context = {'posts': Post.objects.all()}

    def form_valid(self, form):
        self.object = form.save()
        NewsPaper.post.clear()
        post_ids = self.request.POST.getlist("post_ids")
        news_obj = NewsPaper.objects.get(id=self.object.id)
        for id in post_ids:
            post_obj = Post.objects.get(id=int(id))
            news_obj.post.add(post_obj)
        return HttpResponseRedirect(self.get_success_url())
    # def get_context_data(self, *args, **kwargs):
    #     context = super(NewsPaperCreate, self).get_context_data(*args, **kwargs)
    #     context['posts'] = Post.objects.all()
    #     return context


class NewsPaperUpdate(UpdateView):
    model = NewsPaper
    template_name = 'news.html'
    fields = ('name', 'language', 'post')
    extra_context = {'posts': Post.objects.all()}
    context_object_name = "news"

    def get_context_data(self, **kwargs):
        context = super(NewsPaperUpdate, self).get_context_data(**kwargs)
        context["post_list"] = NewsPaper.objects.get(id=self.kwargs["pk"]).post.values_list("id", flat=True)

        return context

    def form_valid(self, form):
        self.object = form.save()
        news = NewsPaper.objects.get(id=self.object.id)
        news.post.clear()

        post_ids = self.request.POST.getlist("post_ids")
        news_obj = NewsPaper.objects.get(id=self.object.id)
        for id in post_ids:
            post_obj = Post.objects.get(id=int(id))
            news_obj.post.add(post_obj)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('news_view')


class NewsPaperDetail(DetailView):
    model = NewsPaper
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super(NewsPaperDetail, self).get_context_data(**kwargs)
        context["posts"] = NewsPaper.objects.get(id=self.kwargs["pk"]).post.all()
        # context["delete_id"] = self.kwargs["pk"]
        return context


class NewsPaperDelete(DeleteView):
    model = NewsPaper
    template_name = "single_news_detail.html"
    success_message = "Deleted Successfully"

    def get_success_url(self):
        return reverse_lazy('news_view')


class PostClassApi(APIView):

    def get(self, request, format=None):
        post = Post.objects.all()
        postserializer = PostSerializer(post, many=True)
        return Response(postserializer.data)

    def post(self, request):
        # content=request.data.dict()
        #
        # content["author"]=User.objects.get(id=int(content["author"]))
        #
        # print(content)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # post=Post.objects.create(**content)
            # post_obj=Post.objects.get(id=post.id)
            # serializer_post = PostSerializer(post_obj)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUpdateDelete(APIView):
    def get_list(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Http404

    def get(self, request, pk):
        post = self.get_list(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_list(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        post = self.get_list(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostMixins(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    queryset = Post.objects.all()

    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostUpdateMixins(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostGenerics(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostGenericsUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class NewsGetCreate(ViewSet):
    def get(self, request):
        news = NewsPaper.objects.all()
        news_obj = NewsPaperSerializer(news, many=True)

        if news:
            response = {"data": news_obj.data, "success": True, "message": "Data in list"}
            status_code = status.HTTP_200_OK
        else:
            response = {"data": "", "success": False, "message": "no data found"}
            status_code = status.HTTP_404_NOT_FOUND
            return Response(response, status_code)
        return Response(response, status_code)

    def create_news(self, request, **data):
        serializer = NewsPaperSerializer(data=request.data)
        if serializer.is_valid():
            post_ids = request.data["post"]
            del request.data["post"]
            # post_ids = post_ids.split(',')
            news_create = NewsPaper.objects.create(**request.data)

            if news_create:
                news_obj = NewsPaper.objects.get(id=news_create.id)
                for id in post_ids:
                    post_obj = Post.objects.get(id=int(id))
                    news_obj.post.add(post_obj)
            news_data = NewsPaper.objects.get(id=news_create.id)
            news_serializer = NewsPaperSerializer(news_data)

        else:
            response = {"data": serializer.errors, "success": False, "message": "data is not created"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status_code)
        response = {"data": news_serializer.data, "success": True, "message": "news created"}
        status_code = status.HTTP_201_CREATED
        return Response(response, status_code)


class NewsUpdateDelete(ViewSet):
    def get(self, request, pk):
        try:
            news_obj = NewsPaper.objects.get(pk=pk)
        except NewsPaper.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        news_obj = NewsPaperSerializer(news_obj)
        if news_obj:
            response = {"data": news_obj.data, "success": True, "message": "data in single id"}
            status_code = status.HTTP_200_OK
        else:
            response = {"data": "no data", "success": False, "message": "data not found"}
            status_code = status.HTTP_404_NOT_FOUND
            return Response(response, status_code)
        return Response(response, status_code)

    def update(self, request, pk):
        news_obj = NewsPaper.objects.get(pk=pk)
        serializer = NewsPaperSerializer(news_obj, data=request.data, partial=True)
        if serializer.is_valid():
            if "post" in request.data:
                post_ids = request.data["post"]
                del request.data["post"]

            news_update = NewsPaper.objects.filter(pk=pk).update(**request.data)

            if news_update:
                if "post" in request.data:
                    news_obj.post.clear()
                    for id in post_ids:
                        post_obj = Post.objects.get(id=int(id))
                        news_obj.post.add(post_obj)

            news_data = NewsPaper.objects.get(pk=pk)

            news_serializer = NewsPaperSerializer(news_data)

        else:
            response = {"data": "no data", "success": False, "message": "not updated"}
            status_code = status.HTTP_404_NOT_FOUND
            return Response(response, status_code)
        response = {"data": news_serializer.data, "success": True, "message": "data is updated"}
        status_code = status.HTTP_200_OK
        return Response(response, status_code)

    def delete(self, request, pk):
        news_obj = NewsPaper.objects.filter(pk=pk)
        if news_obj:
            news_obj.delete()

        else:
            response = {"success": False, "message": "data not found"}
            status_code = status.HTTP_404_NOT_FOUND

            return Response(response, status_code)
        response = {"success": True, "message": "data deleted"}
        status_code = status.HTTP_204_NO_CONTENT
        return Response(response, status_code)


class UserGetCreate(ViewSet):
    def get(self, request):
        user_obj = User.objects.all()
        serializer = UserSerializer(user_obj, many=True)
        if serializer:
            response = {"data": serializer.data, "success": True, "message": "getting user data"}
            status_code = status.HTTP_200_OK
        else:
            response = {"success": False, "message": "no data "}
            status_code = status.HTTP_404_NOT_FOUND
            return Response(response, status_code)
        return Response(response, status_code)

    def create_user(self, request):
        user_obj = UserSerializer(data=request.data)
        if user_obj.is_valid():

            request.data['password'] = make_password(request.data['password'])
            user = User.objects.create(**request.data)
            serializer = UserSerializer(user)
        else:
            response = {"data": user_obj.errors, "success": False, "message": "user is not created"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status_code)
        response = {"data": serializer.data, "success": True, "message": "user created"}
        status_code = status.HTTP_201_CREATED
        return Response(response, status_code)


class UserUpdateDelete(ViewSet):
    def get_user(self, request, pk):
        try:
            user_obj = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        user_detail = UserSerializer(user_obj)
        if user_detail:
            response = {"data": user_detail.data, "success": True, "message": "get user by id"}
            status_code = status.HTTP_200_OK
        else:
            response = {"data": user_detail.errors, "success": False, "message": "no user found"}
            status_code = status.HTTP_404_NOT_FOUND
            return Response(response, status_code)
        return Response(response, status_code)

    def update_user(self, request, pk):
        user_obj = User.objects.get(pk=pk)
        serializer = UserSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            if 'password' in request.data:
                request.data['password'] = make_password(request.data['password'])

                user_update = User.objects.filter(pk=pk).update(**request.data)

        else:
            response = {"data": serializer.errors, "success": False, "message": "data is not updated"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status_code)
        response = {"data": User.objects.filter(pk=pk).values('id', 'first_name'), "success": True,
                    "message": "data is updated"}
        status_code = status.HTTP_200_OK
        return Response(response, status_code)

    def delete_user(self, request, pk):
        try:
            user_obj = User.objects.get(pk=pk)
        except User.DoesNotExist:
            response = {"success": False, "message": "Sorry! data with this id:{} does not exist".format(pk)}
            status_code = status.HTTP_404_NOT_FOUND

            return Response(response, status_code)


        else:
            user_obj.delete()

        response = {"success": True, "message": "data deleted"}
        status_code = status.HTTP_204_NO_CONTENT
        return Response(response, status_code)
