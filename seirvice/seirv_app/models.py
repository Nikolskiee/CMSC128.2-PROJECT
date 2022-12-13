from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here
USER_CHOICES = (
		('Student','Student'),
		('Doctor', 'Doctor')
)

class CustomUser(AbstractUser):
    profession = models.CharField(max_length=100, choices=USER_CHOICES, default='Student')

class InfectiousDisease(models.Model):
	#user = models.ForeignKey(User)
	N_in = models.FloatField()
	t_duration = models.FloatField()
	R0_input = models.FloatField()
	t_incubation = models.FloatField()
	t_infection = models.FloatField()
