from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    avatar=models.ImageField(upload_to='avatars/',blank=True,null=True)
    bio=models.TextField(blank=True)
    job_title=models.CharField(max_length=100,blank=True)

def str(self):
    return f'{self.user.username} Profile' 