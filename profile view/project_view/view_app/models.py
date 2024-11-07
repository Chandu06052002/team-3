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
    uploaded_by = models.CharField(max_length = 250)
    project_start_date = models.DateField()
    project_end_date = models.DateField()
    people_working = models.IntegerField()


# RESOURCES OF THE PROJECT

class MaterialModel(models.Model):
    MATERIAL_CHOICES = [
        ('cement', 'Cement'),
        ('sand', 'Sand'),
        ('bricks', 'Bricks'),
        ('gravel', 'Gravel'),
    ]
    
    material_type = models.CharField(max_length=10, choices=MATERIAL_CHOICES)
    total_quantity = models.IntegerField()
    quantity_used = models.IntegerField()
    quantity_left = models.IntegerField()
    arrival_date = models.DateField()

    def save(self, *args, **kwargs):
        # Automatically calculate quantity_left
        self.quantity_left = self.total_quantity - self.quantity_used
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_material_type_display()} - Total: {self.total_quantity}, Used: {self.quantity_used}, Left: {self.quantity_left}"     



class Worker(models.Model):
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    hired_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='workers')  # Links the worker to the supervisor

    def __str__(self):
        return self.name