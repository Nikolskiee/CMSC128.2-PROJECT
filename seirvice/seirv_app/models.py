from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here
USER_CHOICES = (
		('Student','Student'),
		('Doctor', 'Doctor')
)

class CustomUser(AbstractUser):
    profession = models.CharField(max_length=100, choices=USER_CHOICES, default='Student')
