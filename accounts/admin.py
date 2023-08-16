from django.contrib import admin
from . import models
# Register your models here.






admin.site.register(models.Admin)

admin.site.register(models.Equipment)


admin.site.register(models.Services)
admin.site.register(models.Tickets)
admin.site.register(models.Field)

