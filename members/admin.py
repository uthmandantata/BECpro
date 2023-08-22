from django.contrib import admin
from . import models
# Register your models here.

class PayHistoryAdmin(admin.ModelAdmin):
    list_display = ('user','paystack_charge_id','paystack_access_code','payment_for','amount','activity')
admin.site.register(models.PayHistory,PayHistoryAdmin)


 

admin.site.register(models.Member)

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('membership_type','price','activity','duration')
admin.site.register(models.Membership,MembershipAdmin)


admin.site.register(models.ForgetPassword)
admin.site.register(models.Days)
admin.site.register(models.Features)








