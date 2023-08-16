from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_super_admin = models.BooleanField(null=True, default=False)
    is_admin = models.BooleanField(null=True, default=False)
    is_member = models.BooleanField(null=True, default=False)
    is_allowed = models.BooleanField(null=True, default=False)