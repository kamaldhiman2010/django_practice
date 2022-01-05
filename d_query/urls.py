"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include, reverse
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .import  views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'posts', views.PostViewSet)
from .models import Post, NewsPaper

urlpatterns = [
                  path('', views.post_list, name='post_list'),
                  path('register/', views.register, name='register'),
                  path('set_password/', views.set_password, name='set_password'),
                  path('login/', views.login_custom, name='login'),
                  path('logout/', views.logout_custom, name='logout'),
                  path('post/<int:pk>/', views.post_detail, name='post_detail'),
                  path('post/new/', views.post_new, name='post_new'),
                  path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
                  path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
                  path('new_detail/', views.new_detail, name='new_detail'),
                  path('all_posts/', views.all_posts, name='all_posts'),
                  path('list_post/', views.PostListView.as_view(), name='list_post'),
                  path('detail_post/<int:pk>/', views.PostDetailView.as_view(), name='detail_post'),
                  path('detail_post/<int:pk>/update/', views.PostUpdateView.as_view(), name='update_post'),
                  path('create_post/', views.PostCreateView.as_view(model=Post, success_url='/list_post/'), name='create_post'),
                  path('detail_post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
                  path('all_posts/add_comments/<int:id>/', views.add_comments, name='add_comments'),
                  path('payment_register/',views.payment_register,name='payment_register'),
                  path('new_posts/', views.new_posts, name='new_posts'),
                  path('new_posts/<int:id>/', views.news_edit, name='news_edit'),
                  path('user_listt/', views.user_listt, name='user_listt'),
                  path('user_listt/<int:pk>/', views.user_detail, name='user_detail'),
                #   path('parent_info_new',views.parent_info_new,name='parent_info_new'),
                  path('post_listt/', views.post_listt, name='post_listt'),
                  path('post_listt/<int:id>/', views.postt_detail, name='postt_detail'),
                  path('news_list/', views.news_list, name='news_list'),
                  path('news_list/<int:pk>', views.news_update, name='news_update'),
                  path('news_view/', views.NewsPaperView.as_view(), name='news_view'),
                  path('news_create/', views.NewsPaperCreate.as_view(model=NewsPaper, success_url='/news_view/'), name='news_create'),
                  path('news_view/<int:pk>/update/', views.NewsPaperUpdate.as_view(), name='news_update'),
                  path('news_view/<int:pk>/', views.NewsPaperDetail.as_view(), name='news_detail'),
                  path('news_view/<int:pk>/delete/', views.NewsPaperDelete.as_view(), name='news_delete'),
                  path('get_api/', views.PostClassApi.as_view(), name='get_api'),
                  path('post_api/', views.PostClassApi.as_view(), name='post_api'),
                  path('post_update_delete/<int:pk>/', views.PostUpdateDelete.as_view(), name='post_update_delete'),
                  path('post_mixin_list_create/', views.PostMixins.as_view(), name='post_mixin_list_create'),
                  path('post_mixin_update_destroy/<int:pk>/', views.PostUpdateDelete.as_view(), name='post_mixin_update_destroy'),
                  path('post_generic_list_create/', views.PostGenerics.as_view(), name='post_generic_list_create'),
                  path('post_generic_update_destroy/<int:pk>/', views.PostGenericsUpdate.as_view(), name='post_generic_update_destroy'),
                  path('get/',views.NewsGetCreate.as_view({'get':'get'}),name='get_news'),
                  path('create/',views.NewsGetCreate.as_view({'post':'create_news'}),name='create_news'),
                  path('get/<int:pk>/',views.NewsUpdateDelete.as_view({'get':'get'}),name='get_news'),
                  path('update/<int:pk>/',views.NewsUpdateDelete.as_view({'put':'update'}),name='update_news'),
                  path('delete/<int:pk>/',views.NewsUpdateDelete.as_view({'delete':'delete'}),name='delete_news'),
                  path('getuser/',views.UserGetCreate.as_view({'get':'get'}),name='get_user'),
                  path('createuser/',views.UserGetCreate.as_view({'post':'create_user'}),name='create_user'),
                  path('getuser/<int:pk>/',views.UserUpdateDelete.as_view({'get':'get_user'}),name='get_user'),
                  path('updateuser/<int:pk>/',views.UserUpdateDelete.as_view({'put':'update_user'}),name='update_user'),
                  path('deleteuser/<int:pk>/',views.UserUpdateDelete.as_view({'delete':'delete_user'}),name='delete_user'),
                  path('search/', views.search, name='search'),
                  # path('api/', include(router.urls)),
                  # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
