from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    certifications = models.FileField(
        upload_to='certifications/', blank=True, null=True)
    isifa_number = models.CharField(max_length=100, blank=True, null=True)

    ACCESS_LEVEL_CHOICES = (
        (1, 'Admin'),
        (2, 'Consultant'),
        (3, 'Client'),
    )

    access_level = models.IntegerField(
        choices=ACCESS_LEVEL_CHOICES,
        null=True,
        blank=True
    )

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username
