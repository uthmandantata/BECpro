from django.db import models
from authenticate import models as md


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
    used = models.BooleanField(default=False, null=True)
    quantity = models.IntegerField(default=0)
    total_price = models.CharField(max_length=150, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.customer_fullname)


class Field(models.Model):
    STATUS = (
        ("Closed", "Closed"),
        ("Open", "Open"),
    )
    name = models.CharField(max_length=20, null=True)
    riding_field_status = models.CharField(max_length=20, null=True, choices=STATUS)
    polo_field_status = models.CharField(max_length=20, null=True, choices=STATUS)
    bush_riding_status = models.CharField(max_length=20, null=True, choices=STATUS)
    riding_academy_status = models.CharField(max_length=20, null=True, choices=STATUS)

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
    number_that_needs_repair = models.IntegerField(null=True)
    for_polo = models.BooleanField(default=True, null=True)
    date_bought = models.DateField(null=True)

    def __str__(self):
        return self.name


class Admin(models.Model):
    user = models.OneToOneField(
        md.CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    # Add your admin fields here


class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(md.CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user} --- {self.timestamp}"
