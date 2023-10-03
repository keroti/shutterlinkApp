from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Services(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=500)


class PhotographerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact_information = models.CharField(max_length=255)
    email = models.EmailField()
    birth_date = models.DateField(blank=True, null=True)
    twitter = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    service_details = models.TextField()
    brief_description = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pic/', null=True, blank=True)

    def __str__(self):
        return self.name
