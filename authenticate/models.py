from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_super_admin = models.BooleanField(null=True, default=False)
    is_admin = models.BooleanField(null=True, default=False)
    is_member = models.BooleanField(null=True, default=False)
    is_allowed = models.BooleanField(null=True, default=False)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    email =models.CharField(max_length=150, unique=True)
    username =models.CharField(max_length=150, unique=True, null=True)
    phone =models.CharField(max_length=150, null=True)
    age = models.IntegerField(default=18)
    address = models.CharField(max_length=150, null=True)
    city = models.CharField(max_length=150, null=True)
    postal_code = models.CharField(max_length=150, null=True)
    
    
    # room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.email} Profile'