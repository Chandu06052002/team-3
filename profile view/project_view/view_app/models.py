from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Optionally, add related_name to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Avoid reverse accessor conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Avoid reverse accessor conflict
        blank=True
    )

    def __str__(self):
        return self.username

class Imagemodel(models.Model):
    project_name = models.CharField(max_length=250)
    project_image = models.FileField(upload_to='Document/')
    project_location = models.CharField(max_length = 250)
    Uploader_name = models.CharField(max_length = 250)
    project_start_date = models.DateField()
    project_end_date = models.DateField()
    people_working = models.IntegerField()