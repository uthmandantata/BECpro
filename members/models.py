from django.db import models
from authenticate import models as md

class Profile(models.Model):
    user = models.OneToOneField(md.CustomUser, on_delete=models.CASCADE,null=True, blank=True)
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
        return 'f{self.email} Profile'

class ForgetPassword(models.Model):
    user = models.OneToOneField(md.CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    forget_password_token = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return str(self.user)
   
class Day1(models.Model):
    DAYS = (
        ('Sunday','Sunday'),
    )
    TIME_SLOT = (
        ('8-10 am', '8-10 am'),
        ('4-6 pm', '4-6 pm'),
    )
    name = models.CharField(max_length=200, null=True)
    days = models.CharField(max_length=200, null=True, choices=DAYS)
    time_slot = models.CharField(max_length=200, null=True, choices=TIME_SLOT)
    amount = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.name)
    
class Day2(models.Model):
    DAYS = (
        ('Wednesday','Wednesday'),

    )
    TIME_SLOT = (
        ('8-10 am', '8-10 am'),
        ('4-6 pm', '4-6 pm'),
    )
    name = models.CharField(max_length=200, null=True)
    days = models.CharField(max_length=200, null=True, choices=DAYS)
    time_slot = models.CharField(max_length=200, null=True, choices=TIME_SLOT)
    amount = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.name)
    
class Day3(models.Model):
    DAYS = (
        ('Saturday','Saturday'),
    )
    TIME_SLOT = (
        ('8-10 am', '8-10 am'),
        ('4-6 pm', '4-6 pm'),
    )
    name = models.CharField(max_length=200, null=True)
    days = models.CharField(max_length=200, null=True, choices=DAYS)
    time_slot = models.CharField(max_length=200, null=True, choices=TIME_SLOT)
    amount = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.name)
    
class Membership(models.Model):
    MEMBERSHIP = (
        ('Family Riding Monthly', 'Family Riding Monthly'),
        ('Family Riding Yearly', 'Family Riding Yearly'),
        ('Family Polo Monthly', 'Family Polo Monthly'),
        ('Family Polo Yearly', 'Family Polo Yearly'),
        ('Single Riding Monthly', 'Single Riding Monthly'),
        ('Single Riding Yearly', 'Single Riding Yearly'),
        ('Single Polo Monthly', 'Single Polo Monthly'),
        ('Single Polo Yearly', 'Single Polo Yearly'),
        
    )
    ACTIVITY = (
        ('Riding', 'Riding'),
        ('Polo', 'Polo'),
    )
    DURATION = (
        (' Monthly', ' Monthly'),
        (' Yearly', ' Yearly'),
        
    )
   
 
    membership_type = models.CharField(max_length=150, choices=MEMBERSHIP)
    price = models.IntegerField(null=True)
    activity  =models.CharField(max_length=150, null=True, choices=ACTIVITY)
    duration =models.CharField(max_length=150, null=True, choices=DURATION)
    duration_in_months =models.CharField(max_length=150, null=True)
   

    def __str__(self):
        return self.membership_type

class PayHistory(models.Model):
    user = models.ForeignKey(md.CustomUser, on_delete=models.CASCADE, default=None)
    paystack_charge_id = models.CharField(max_length=100, blank=True)
    paystack_access_code = models.CharField(max_length=100, blank=True)
    payment_for = models.ForeignKey('Membership', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    activity = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(null=True, default=False)
    date_paid = models.DateTimeField(null=True)
    expiry_date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.user)

class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(md.CustomUser, on_delete=models.CASCADE)
    


