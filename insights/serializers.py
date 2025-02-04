from rest_framework import serializers
from .models import Page, Post, SocialMediaUser

class SocialMediaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaUser
        fields = ['id', 'name', 'profile_pic', 'fb_id']

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'likes', 'shares', 'timestamp']

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaUser
        fields = ['id', 'name', 'profile_pic', 'fb_id']