from django.contrib import admin
from . import models
# Register your models here.


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('membership_type','price','activity','duration')
admin.site.register(models.Membership,MembershipAdmin)






class PayHistoryAdmin(admin.ModelAdmin):
    list_display = ('user','paystack_charge_id','paystack_access_code','payment_for','amount','activity')
admin.site.register(models.PayHistory,PayHistoryAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('is_read','message','timestamp','user')
admin.site.register(models.Notification,NotificationAdmin)
 

admin.site.register(models.Profile)
admin.site.register(models.Admin)
admin.site.register(models.Member)
admin.site.register(models.Equipment)
admin.site.register(models.Horses)
admin.site.register(models.ForgetPassword)
admin.site.register(models.Day1)
admin.site.register(models.Day2)
admin.site.register(models.Day3)

admin.site.register(models.Services)
admin.site.register(models.Tickets)
admin.site.register(models.Field)

