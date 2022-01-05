from django.contrib.auth.decorators import permission_required
import requests
from django.conf import Settings
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.functions import Length
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
class PostManager(models.Manager):
    def get_queryset(self):
        return super(PostManager, self).get_queryset().filter(title__startswith='f')


class PostQuerySet(models.QuerySet):
    def long_first_name(self):
        return self.annotate(length=Length("title")).filter(length__gte=10)

    def short_last_name(self):
        return self.annotate(length=Length("subject")).filter(length__lte=5)


class PostAuthorManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def long_first_name(self):
        return self.get_queryset().long_first_name()

    def short_last_name(self):
        return self.get_queryset().short_last_name()


class Post(models.Model):
    title = models.CharField(max_length=20)
    subject = models.TextField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/', blank=True)
    video = models.FileField(upload_to='video/', blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    post_objects = PostManager()
    post_obj=PostAuthorManager()

    class Meta:
        permissions=[("can_view", "Can view the post"),
            ("can_delete", "Can delete the post"),
            ("can_edit","can edit the post")]


    


    def snippet(self):
        return self.subject[:50] + '...'

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    


class NewsPaper(models.Model):
    name = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    post = models.ManyToManyField(Post, blank=True)
    def __str__(self):
        return self.name


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comments = models.CharField(max_length=100, null=True)


class MultipleUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GROUP_CHOICE = (
        ('S', 'STAFF'),
        ('C', 'CUSTOMER'),
    )
    choice_field = models.CharField(max_length=20, choices=GROUP_CHOICE)


class Payment(models.Model):
    User= models.ForeignKey(User,on_delete=models.CASCADE)
    invoiceid = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    amount = models.DecimalField(decimal_places=2, max_digits=20,null=True)
    email = models.EmailField(max_length=255, blank=False, null=False)
    phone = models.CharField(max_length=11, blank=False, null=False)
    clientid = models.IntegerField(blank=True, null=True, unique=False)


