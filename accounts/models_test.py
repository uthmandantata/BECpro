from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone




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
        return 'f{self.email} Profile'


class ForgetPassword(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    forget_password_token = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return str(self.user)
    

class Services(models.Model):
    name = models.CharField(max_length=150, null=True)
    duration = models.CharField(max_length=150, null=True)
    explanation = models.CharField(max_length=150, null=True)
    price = models.IntegerField()

    def __str__(self):
        return str(self.name)
    


class Tickets(models.Model):
    ticket_number = models.CharField(max_length=150, null=True)
    attendant = models.CharField(max_length=150, null=True)
    customer_fullname = models.CharField(max_length=150, null=True)
    customer_email = models.CharField(max_length=150, null=True)
    customer_number = models.CharField(max_length=150, null=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total_price = models.CharField(max_length=150, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.customer_fullname)

class Slots(models.Model):
    DAYS = (
        ('Sunday','Sunday'),
        ('Friday','Friday'),
        ('Wednesday','Wednesday'),
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    

class Member(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE,null=True, blank=True)
    activity  =models.CharField(max_length=150, null=True)
    paid = models.BooleanField(default=False)
    day1 = models.ForeignKey(Day1, on_delete=models.CASCADE,null=True, blank=True)
    day2 = models.ForeignKey(Day2, on_delete=models.CASCADE,null=True, blank=True)
    day3 = models.ForeignKey(Day3, on_delete=models.CASCADE,null=True, blank=True)
    suspend = models.BooleanField(default=False)
    # day3 = models.ForeignKey(Slots, on_delete=models.CASCADE,null=True, blank=True)
    email = models.CharField(max_length=150, null=True)

    guardian_name = models.CharField(max_length=150, null=True)
    guardian_age = models.IntegerField(null=True)
    guardian_weight = models.IntegerField(null=True)
    guardian_height = models.IntegerField(null=True)

    member1_full_name = models.CharField(max_length=150, null=True)
    member1_age = models.IntegerField(null=True)
    member1_email = models.CharField(max_length=150, null=True)
    member1_weight = models.IntegerField(null=True)
    member1_height = models.IntegerField(null=True)
    member1_address = models.CharField(max_length=150, null=True)
    member1_city = models.CharField(max_length=150, null=True)

    member2_full_name = models.CharField(max_length=150, null=True)
    member2_age = models.IntegerField(null=True)
    member2_email = models.CharField(max_length=150, null=True)
    member2_weight = models.IntegerField(null=True)
    member2_height = models.IntegerField(null=True)
    member2_address = models.CharField(max_length=150, null=True)
    member2_city = models.CharField(max_length=150, null=True)
    
    date_paid = models.DateField(null=True)
    paid_until = models.DateField(null=True)
    
    # room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.guardian_name


class Field(models.Model):
    STATUS = (
        ('Closed', 'Closed'),
        ('Open', 'Open'),
    )
    name = models.CharField(max_length=20,null=True)
    riding_field_status = models.CharField(max_length=20,null=True, choices=STATUS)
    polo_field_status = models.CharField(max_length=20,null=True, choices=STATUS)
    bush_riding_status = models.CharField(max_length=20,null=True, choices=STATUS)
    riding_academy_status = models.CharField(max_length=20,null=True, choices=STATUS)

    def __str__(self):
        return str(self.name)
    

class Horses(models.Model):
    name = models.CharField(max_length=150, null=True)
    age = models.IntegerField(null=True)
    date_bought = models.DateField(null=True)
    weight = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    for_polo = models.BooleanField(null=True, default=True)

    def __str__(self):
        return str(self.name)



class Equipment(models.Model):
    name = models.CharField(max_length=150, null=True)
    amount = models.IntegerField(null=True)
    price_bought = models.IntegerField(null=True)
    needs_repair = models.BooleanField(null=True, default=False)
    def __str__(self):
        return self.name


class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    # Add your admin fields here



