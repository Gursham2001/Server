from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=250, default='https://www.pngitem.com/pimgs/m/150-1503945_transparent-user-png-default-user-image-png-png.png')
    job_title = models.CharField(max_length=100, blank=True)
    gacohort = models.CharField(max_length=50, blank=True)
    linkedin = models.CharField(max_length=250, blank=True)
    github = models.CharField(max_length=250, blank=True)
    instagram = models.CharField(max_length=250, blank=True)
    twitter = models.CharField(max_length=250, blank=True)
    personalsite= models.CharField(max_length=250, blank=True)
    created_project = models.CharField(max_length= 250, blank=True)