from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_img', null=True, blank=True)
    about = models.TextField(default="", blank=True)
    def __str__(self):
        return f'{self.user.username } , {self.about}'

class Post(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='post_img', null=True, blank=True)
    post_title = models.TextField(default="", blank=True)
    post_description = models.TextField(default="", blank=True)
    post_file = models.FileField(upload_to='post_file', null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)