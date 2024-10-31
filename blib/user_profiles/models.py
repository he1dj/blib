from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)

    def __str__(self):
        return self.user.email
    