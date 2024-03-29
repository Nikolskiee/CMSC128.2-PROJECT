from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here
USER_CHOICES = (
		('Student','Student'),
		('Hospital Staff', 'Hospital Staff')
)

MASK_CHOICES = (
	('Yes', 'Yes'),
	('No', 'No')
)
class CustomUser(AbstractUser):
    profession = models.CharField(max_length=100, choices=USER_CHOICES, default='Student')

class InfectiousDisease(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	N_in = models.FloatField()
	t_duration = models.FloatField()
	R0_input = models.FloatField()
	t_incubation = models.FloatField()
	t_infection = models.FloatField()
	E_in  = models.FloatField()
	I_in = models.FloatField()
	R_in = models.FloatField()
	v_eff = models.FloatField()
	mask_use = models.CharField(max_length=100, choices=MASK_CHOICES, default='No')
	created_at = models.DateTimeField(auto_now_add=True)
	cov_val = models.FloatField()


class Dengue(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	N_h = models.FloatField()
	N_v = models.FloatField()
	t_duration = models.FloatField()
	bite_n = models.FloatField()
	bv_input = models.FloatField()
	bh_input = models.FloatField()
	uv_input = models.FloatField()
	h_recov_input = models.FloatField()
	Ih_in = models.FloatField()
	Rh_in = models.FloatField()
	Iv_in = models.FloatField()
	created_at = models.DateTimeField(auto_now_add=True)
	