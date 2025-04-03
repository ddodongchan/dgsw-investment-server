from django.db import models

# Create your models here.

class User(models.Model):
    class RoleChoices(models.TextChoices):
        REPORTER = "reporter", "Reporter"
        USER = "user", "User"
        ADMIN = "admin", "Admin"

    name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.USER)
