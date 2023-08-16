from django.contrib import admin
from . import models
# Register your models here.


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('membership_type','price','activity','duration')
admin.site.register(models.Membership,MembershipAdmin)



admin.site.register(models.Admin)
admin.site.register(models.Member)
admin.site.register(models.Equipment)


admin.site.register(models.Services)
admin.site.register(models.Tickets)
admin.site.register(models.Field)

