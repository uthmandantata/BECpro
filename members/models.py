from django.db import models
from authenticate import models as md
from staff import models as amd

class ForgetPassword(models.Model):
    user = models.OneToOneField(md.CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    forget_password_token = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.user)
   
class Days(models.Model):
    NAME = (
        ('Saturday Morning','Saturday Morning'),
        ('Saturday Evening','Saturday Evening'),
        ('Sunday Morning','Sunday Morning'),
        ('Sunday Evening','Sunday Evening'),
        ('Wednesday Morning','Wednesday Morning'),
        ('Wednesday Evening','Wednesday Evening'),
        ('Friday Morning','Friday Morning'),
        ('Friday Evening','Friday Evening'),
      
    )
    DAYS = (
        ('Saturday','Saturday'),
        ('Sunday','Sunday'),
        ('Wednesday','Wednesday'),
        ('Friday','Friday'),
    )
    TIME_SLOT = (
        ('8-10 am', '8-10 am'),
        ('4-6 pm', '4-6 pm'),
    )
    name = models.CharField(max_length=200, null=True, choices=NAME)
    days = models.CharField(max_length=200, null=True, choices=DAYS)
    time_slot = models.CharField(max_length=200, null=True, choices=TIME_SLOT)
    amount = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return str(self.name)
 
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
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.user)



class Features(models.Model):
    ACTIVITY = (
        ('POLO','POLO'),
        ('RIDING','RIDING'),
    )
    
    activity = models.CharField(max_length=150,null=True, choices=ACTIVITY)
    features = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.features

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
    description =models.TextField(null=True)
    features = models.ManyToManyField(Features)
    duration_in_months =models.CharField(max_length=150, null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
   

    def __str__(self):
        return self.membership_type

class Member(models.Model):
    user = models.OneToOneField(md.CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE,null=True, blank=True)
    activity  = models.CharField(max_length=150, null=True)
    paid = models.BooleanField(default=False)
    days = models.ManyToManyField(Days)
    # day2 = models.ForeignKey(Day2, on_delete=models.CASCADE,null=True, blank=True)
    # day3 = models.ForeignKey(Day3, on_delete=models.CASCADE,null=True, blank=True)
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
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    
    # room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
