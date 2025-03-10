# Generated by Django 5.0.2 on 2025-02-04 08:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=500)),
                ('fb_id', models.CharField(max_length=255)),
                ('profile_pic', models.URLField(max_length=500)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('website', models.URLField(blank=True)),
                ('category', models.CharField(max_length=255)),
                ('followers_count', models.IntegerField(default=0)),
                ('likes_count', models.IntegerField(default=0)),
                ('creation_date', models.DateField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialMediaUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('profile_pic', models.URLField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_post_id', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('shares', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField()),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='insights.page')),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='followers',
            field=models.ManyToManyField(related_name='following_pages', to='insights.socialmediauser'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='insights.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insights.socialmediauser')),
            ],
        ),
    ]
