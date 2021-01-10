from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Section(models.Model):
    name = models.CharField(max_length=100)


class Article(models.Model):
    name = models.CharField(max_length=200)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    section_id = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField()
    edited_date = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=False)
    path = models.CharField(max_length=200)


class Tag(models.Model):
    article_id = models.ManyToManyField(Article, db_table='articles_to_tags')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)


class Comment(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class User(AbstractUser):
    pass


# class Role(models.Model): # can be replaced by the 'Group' - standard Django class associated with User
#     name = models.CharField
