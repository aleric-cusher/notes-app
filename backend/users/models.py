from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True)
    date_of_birth = models.DateField(null=True)
    
    def __str__(self) -> str:
        return f'{self.profile_picture}'