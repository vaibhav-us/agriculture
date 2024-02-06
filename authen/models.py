from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_photo = models.TextField(max_length=200)
    nick_name = models.TextField(max_length=60)
    place = models.TextField(max_length=200,default="kozhikode")

    def __str__(self):
        return self.user.username

class Crop(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=50)
    crop_stage =models.TextField(max_length=50)
    crop_area =models.TextField(max_length=50)

    def __str__(self):
        return self.crop_name



