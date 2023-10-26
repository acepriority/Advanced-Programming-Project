from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Custom fields
    officer_id = models.CharField(max_length=15, unique=True)
    dob = models.DateField()
    contact = models.CharField(max_length=13)
    sex = models.CharField(max_length=1)
    nin = models.CharField(max_length=14, unique=True)
    position = models.CharField(max_length=50)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class ResidencyProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
        )
    country = models.CharField(max_length=255)
    district_city = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    parish = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
