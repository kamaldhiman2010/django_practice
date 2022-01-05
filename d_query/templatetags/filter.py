from django import template
from django.contrib.auth.models import User

from d_query.models import Post, MultipleUsers

import django_filters
register = template.Library()


@register.filter()
def low(value):
    return value.lower()


@register.filter()
def up(value):
    return value.upper()


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['title']


@register.filter(name='get_color')
def color(value):
    if value:
        return "#FF0000"


@register.simple_tag(name='my_posts')
def my_posts():
    return Post.objects.all().count()


@register.filter('show_user')
def show_users(value):
    obj = User.objects.values('username', 'is_staff')

    return obj


@register.filter(name="profile")
def profile(value):
    if value.is_staff:
        return "{} is staff".format(value.username)
    else:
        return "{} is customer".format(value.username)


@register.filter(name="even_no")
def even_no(value):
    listX=[x for x in value if x % 2 == 0]
    return listX

