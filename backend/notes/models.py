from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Color(models.Model):
    id = models.CharField(max_length=20)
    color = models.CharField(max_length=7)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Tag(models.Model):
    id = models.CharField(max_length=20)
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    

class Note(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    tags = models.ManyToManyField(Tag)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
