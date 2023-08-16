from django.contrib import admin
from . import models
# Register your models here.

class PayHistoryAdmin(admin.ModelAdmin):
    list_display = ('user','paystack_charge_id','paystack_access_code','payment_for','amount','activity')
admin.site.register(models.PayHistory,PayHistoryAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('is_read','message','timestamp','user')
admin.site.register(models.Notification,NotificationAdmin)
 

admin.site.register(models.Profile)
admin.site.register(models.Membership)


admin.site.register(models.ForgetPassword)
admin.site.register(models.Day1)
admin.site.register(models.Day2)
admin.site.register(models.Day3)






