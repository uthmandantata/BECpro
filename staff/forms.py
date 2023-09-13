from django import forms
from .models import Equipment, Horses, Services, Tickets, Notification
from authenticate import models as md
from members import models as member_models
from django.contrib.auth.forms import UserCreationForm


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = md.CustomUser
        fields = ("username", "is_super_admin", "is_admin", "is_member")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = md.Profile
        fields = ("first_name", "last_name", "email", "phone", "address")


class MembershipForm(forms.ModelForm):
    class Meta:
        model = member_models.Membership
        fields = "__all__"


class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = member_models.Member
        fields = (
            "email",
            "guardian_name",
            "guardian_age",
            "guardian_weight",
            "guardian_height",
            "member1_full_name",
            "member1_age",
            "member1_email",
            "member1_weight",
            "member1_height",
            "member1_address",
            "member2_full_name",
            "member2_age",
            "member2_email",
            "member2_weight",
            "member2_height",
            "member2_address",
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        return instance


class MemberForm(forms.ModelForm):
    class Meta:
        model = member_models.Member
        fields = (
            "guardian_name",
            "guardian_age",
            "guardian_weight",
            "guardian_height",
            "email",
            "days",
        )

        def __init__(self, *args, **kwargs):
            super(MemberForm, self).__init__(*args, **kwargs)
            self.fields["membership"].disabled = True


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = "__all__"
        widgets = {
            "date_bought": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }


class ForgetPasswordForm(forms.ModelForm):
    class Meta:
        model = member_models.ForgetPassword
        fields = "__all__"


class HorsesForm(forms.ModelForm):
    class Meta:
        model = Horses
        fields = "__all__"
        widgets = {
            "date_bought": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = "__all__"


class TicketsForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = (
            "customer_fullname",
            "customer_email",
            "customer_number",
            "service",
            "quantity",
        )


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ("message",)
