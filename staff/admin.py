from django.contrib import admin
from . import models

# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("is_read", "message", "timestamp", "user")


admin.site.register(models.Notification, NotificationAdmin)

admin.site.register(models.Services)
admin.site.register(models.Tickets)
admin.site.register(models.Field)
admin.site.register(models.Equipment)
admin.site.register(models.Horses)
