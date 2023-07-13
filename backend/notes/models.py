from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Color(models.Model):
    slug = models.CharField(max_length=20, unique=True, blank=True)
    color = models.CharField(max_length=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Tag(models.Model):
    slug = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.slug}-> {self.name}'
    

class Note(models.Model):
    slug = models.CharField(max_length=20, unique=True, blank=True)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    tags = models.ManyToManyField(Tag)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField()
    archived = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)