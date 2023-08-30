from django.db import models
from authenticate import models as md

<<<<<<< HEAD



=======
>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2
class Services(models.Model):
    name = models.CharField(max_length=150, null=True)
    duration = models.CharField(max_length=150, null=True)
    explanation = models.CharField(max_length=150, null=True)
    price = models.IntegerField()

    def __str__(self):
        return str(self.name)
    
<<<<<<< HEAD


=======
>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2
class Tickets(models.Model):
    ticket_number = models.CharField(max_length=150, null=True)
    attendant = models.CharField(max_length=150, null=True)
    customer_fullname = models.CharField(max_length=150, null=True)
    customer_email = models.CharField(max_length=150, null=True)
    customer_number = models.CharField(max_length=150, null=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
<<<<<<< HEAD
=======
    used = models.BooleanField(default=False, null=True)
>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2
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

<<<<<<< HEAD



=======
>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2
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
    
<<<<<<< HEAD

=======
>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2
class Horses(models.Model):
    name = models.CharField(max_length=150, null=True)
    age = models.IntegerField(null=True)
    date_bought = models.DateField(null=True)
    weight = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    for_polo = models.BooleanField(null=True, default=True)

    def __str__(self):
        return str(self.name)

<<<<<<< HEAD


=======
>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2
class Equipment(models.Model):
    name = models.CharField(max_length=150, null=True)
    amount = models.IntegerField(null=True)
    price_bought = models.IntegerField(null=True)
<<<<<<< HEAD
    needs_repair = models.BooleanField(null=True, default=False)
    def __str__(self):
        return self.name


=======
    number_that_needs_repair = models.IntegerField(null=True)
    for_polo = models.BooleanField(default=True, null=True)
    date_bought = models.DateField(null=True)
    
    def __str__(self):
        return self.name

>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2
class Admin(models.Model):
    user = models.OneToOneField(md.CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    # Add your admin fields here


<<<<<<< HEAD
=======
class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(md.CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"{self.user} --- {self.timestamp}"
>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2

