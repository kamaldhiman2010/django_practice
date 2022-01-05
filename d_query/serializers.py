from django.contrib.auth.models import User

from rest_framework import serializers

from django.conf import settings
from .models import Post, NewsPaper
from .forms import UserRegisterForm


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class PostSerializer(serializers.ModelSerializer):

    #author = UserSerializer(many=True, required=False,read_only=True)
    author= serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=User.objects.all()
    )

    class Meta:
        model = Post
        fields = "__all__"
        depth = 1



class NewsPaperSerializer(serializers.ModelSerializer):
    # post = serializers.StringRelatedField()
    # post = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Post.objects.all()
    # )
    class Meta:
        model=NewsPaper
        fields=['name','language','post']
        depth=1  # give detail of post rather then its id


# class PostSerializer(serializers.Serializer):
#
#     images = serializers.ImageField(required=False, allow_null=True)
#     video = serializers.FileField(allow_empty_file=True, required=False,allow_null=True)
#
#     title = serializers.CharField(max_length=100)
#     subject = serializers.CharField(style={'base_template': 'textarea.html'})
#
#     def create(self, validated_data):
#         if "author" in validated_data:
#             user_obj = User.objects.get(id=validated_data["author"])
#             validated_data["author"] = user_obj
#         return Post.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.author = validated_data.get('author', instance.author)
#         instance.images = validated_data.get('images', instance.images)
#         instance.video = validated_data.get('video', instance.video)
#         instance.title = validated_data.get('title', instance.title)
#         instance.subject = validated_data.get('subject', instance.subject)
#         instance.published_date = validated_data.get('published_date', instance.published_date)
#         instance.save()
#         return instance
