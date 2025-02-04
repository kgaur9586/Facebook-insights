from django.db import models

class SocialMediaUser(models.Model):
    fb_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    profile_pic = models.URLField(max_length=500, blank=True)
    
class Page(models.Model):
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=500)
    fb_id = models.CharField(max_length=255)
    profile_pic = models.URLField(max_length=500)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    category = models.CharField(max_length=255)
    followers_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    creation_date = models.DateField(null=True)
    followers = models.ManyToManyField(SocialMediaUser, related_name='following_pages')
    updated_at = models.DateTimeField(auto_now=True)

class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
    fb_post_id = models.CharField(max_length=255)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    timestamp = models.DateTimeField()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(SocialMediaUser, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField()