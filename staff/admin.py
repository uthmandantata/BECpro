from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from . import models
# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('is_read','message','timestamp','user')
admin.site.register(models.Notification,NotificationAdmin)

admin.site.register(models.Services)
admin.site.register(models.Tickets)
admin.site.register(models.Field)
admin.site.register(models.Slots)
admin.site.register(models.Equipment)
admin.site.register(models.Horses)





>>>>>>> 3d40901ea8dc265b5366c0af6bbc19d7433d0ce2
