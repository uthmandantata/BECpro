from django.contrib import admin
from . import models
# Register your models here.

class PayHistoryAdmin(admin.ModelAdmin):
    list_display = ('user','paystack_charge_id','paystack_access_code','payment_for','amount','activity')
admin.site.register(models.PayHistory,PayHistoryAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('is_read','message','timestamp','user')
admin.site.register(models.Notification,NotificationAdmin)
 

admin.site.register(models.Member)

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('membership_type','price','activity','duration')
admin.site.register(models.Membership,MembershipAdmin)


admin.site.register(models.ForgetPassword)
admin.site.register(models.Day1)
admin.site.register(models.Day2)
admin.site.register(models.Day3)





